import re
import logging
from typing import Any

import polars as pl

from utils.attribute import (
    get_access_value,
    get_modified_write_value,
    get_read_action_value,
)


def parse_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    parsed_df = (
        df.with_columns(
            header_reg=pl.first("REG").over("ADDR"),
            start_addr_str=pl.first("ADDR").over("ADDR"),
            stride=(
                pl.col("WIDTH")
                .filter(pl.col("FIELD").is_not_null() & (pl.col("FIELD") != ""))
                .sum()
                .over("ADDR")
                // 8  # 1Byte = 8bits
            ),
        )
        .with_columns(
            is_expandable=pl.col("header_reg").str.contains(r"\{n\}"),
            base_reg_name=pl.coalesce(
                pl.col("header_reg").str.extract(r"(.*?)\{n\}"), pl.lit("")
            ),
            n_start=pl.col("header_reg")
            .str.extract(r"n\s*=\s*(\d+)", 1)
            .cast(pl.Int64),
            n_end=pl.col("header_reg").str.extract(r"~\s*(\d+)", 1).cast(pl.Int64),
            start_addr_int=pl.col("start_addr_str")
            .str.extract(r"0x([0-9a-fA-F]+)")
            .str.to_integer(base=16, strict=True),
        )
        .with_columns(
            n_series=pl.when(
                pl.col("is_expandable")
                & pl.col("n_start").is_not_null()
                & pl.col("n_end").is_not_null()
            )
            .then(pl.int_ranges(pl.col("n_start"), pl.col("n_end") + 1))
            .otherwise(pl.lit(None))
        )
        .explode("n_series")
        .filter(
            (pl.col("is_expandable") & pl.col("n_series").is_not_null())
            | (
                ~pl.col("is_expandable")
                & pl.col("FIELD").is_not_null()
                & (pl.col("FIELD") != "")
            )
        )
        .with_columns(
            ADDR=pl.when(pl.col("is_expandable"))
            .then(
                (
                    pl.col("start_addr_int") + pl.col("n_series") * pl.col("stride")
                ).map_elements(lambda x: f"0x{x:X}", return_dtype=pl.String)
            )
            .otherwise(pl.col("ADDR")),
            REG=pl.when(pl.col("is_expandable"))
            .then(pl.col("base_reg_name") + "_" + pl.col("n_series").cast(pl.String))
            .otherwise(pl.col("REG")),
        )
    )

    parsed_df = parsed_df.select(
        "ADDR",
        "REG",
        "FIELD",
        "BIT",
        "WIDTH",
        "ATTRIBUTE",
        "DEFAULT",
        "DESCRIPTION",
        "stride",
    )

    return parsed_df


def process_vendor_sheet(df: pl.DataFrame, object_factory: Any) -> Any:
    """Process the Sheet<vendor> to create an IP-XACT Component object"""
    try:

        def get_tag_value(tag: str) -> str:
            value = df.filter(pl.col("TAG") == tag)["VALUE"]
            if value.is_empty():
                raise ValueError(f"Tag '{tag}' not found in the Sheet<vendor> ")
            return str(value[0])

        component = object_factory.createComponentType()
        component.setVendor(get_tag_value("VENDOR"))
        component.setLibrary(get_tag_value("LIBRARY"))
        component.setName(get_tag_value("NAME"))
        component.setVersion(get_tag_value("VERSION"))

        return component
    except (pl.exceptions.PolarsError, ValueError, KeyError) as e:
        logging.error(f"Failed to process the Sheet<vendor>: {e}")
        return None
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while processing the Sheet<vendor>: {e}"
        )
        return None


def process_address_map_sheet(df: pl.DataFrame, object_factory: Any) -> list[Any]:
    """Process the Sheet<address_map> to create a list of IP-XACT AddressBlock objects."""
    address_blocks = []
    for row in df.iter_rows(named=True):
        try:
            base_address = object_factory.createUnsignedLongintExpression()
            base_address.setValue(str(row["OFFSET"]))
            block_range = object_factory.createUnsignedPositiveLongintExpression()
            block_range.setValue(str(row["RANGE"]))
            width = object_factory.createUnsignedIntExpression()
            width.setValue("32")
            address_block = object_factory.createAddressBlockType()
            address_block.setName(str(row["BLOCK"]))
            address_block.setBaseAddress(base_address)
            address_block.setRange(block_range)
            address_block.setWidth(width)
            address_blocks.append(address_block)
        except KeyError as e:
            logging.error(
                f"Missing expected column in address_map sheet: {e}. Skipping row: {row}"
            )
    return address_blocks


def process_register_sheet(
    df: pl.DataFrame,
    object_factory: Any,
    AccessType: Any,
    ModifiedWriteValueType: Any,
    ReadActionType: Any,
) -> list[Any]:
    """Process a single register block sheet into a list of Register objects."""
    try:
        # Pre-process the dataframe
        filled_df = df.select(pl.all().forward_fill())
        logging.debug(f"filled_df is {filled_df}")
        parsed_df = parse_dataframe(filled_df)
        logging.debug(f"parsed_df is {parsed_df}")
    except pl.exceptions.PolarsError as e:
        logging.error(f"Polars error during pre-processing of a register sheet: {e}")
        return []

    registers = []
    # Group by register to process all its fields together
    for reg_name, group in parsed_df.group_by("REG", maintain_order=True):
        if not reg_name:
            logging.warning("Skipping rows with no register name.")
            continue

        fields: list[Any] = []
        first_row = group.row(0, named=True)

        for field_row in group.iter_rows(named=True):
            try:
                bit_match = re.findall(r"\[(?:\d+:)?(\d+)]", str(field_row["BIT"]))
                if not bit_match:
                    raise ValueError(
                        f"Could not parse bit offset from '{field_row['BIT']}"
                    )

                if re.match(r"^(rsvd|reserved)\d*$", str(field_row["FIELD"])):
                    continue

                field = object_factory.createFieldType()
                bit_offset = object_factory.createUnsignedIntExpression()
                bit_offset.setValue(str(bit_match[0]))
                bit_width = object_factory.createUnsignedPositiveIntExpression()
                bit_width.setValue(str(field_row["WIDTH"]))
                field.setName(str(field_row["FIELD"]))
                field.setBitOffset(bit_offset)
                field.setBitWidth(bit_width)
                if (access_value := get_access_value(str(field_row["ATTRIBUTE"]))) is not None:
                    field.setAccess(AccessType.fromValue(access_value))
                if (modified_write_value := get_modified_write_value(
                    str(field_row["ATTRIBUTE"])
                )) is not None:
                    modified_write = object_factory.createFieldTypeModifiedWriteValue()
                    modified_write.setValue(ModifiedWriteValueType.fromValue(
                        modified_write_value
                    ))
                    field.setModifiedWriteValue(modified_write)
                if (read_action_value := get_read_action_value(
                    str(field_row["ATTRIBUTE"])
                )) is not None:
                    read_action = object_factory.createFieldTypeReadAction()
                    read_action.setValue(ReadActionType.fromValue(read_action_value))
                    field.setReadAction(read_action)
                resets = object_factory.createFieldTypeResets()
                reset = object_factory.createReset()
                reset_value = object_factory.createUnsignedBitVectorExpression()
                reset_value.setValue(str(field_row["DEFAULT"]))
                reset.setValue(reset_value)
                reset_list = resets.getReset()
                reset_list.add(reset)
                field.setResets(resets)

                fields.append(field)
            except (KeyError, ValueError, TypeError) as e:
                logging.error(
                    f"Skipping invalid field '{field_row.get('FIELD', 'N/A')}' in register '{reg_name[0]}': {e}"
                )

        if fields:
            register = object_factory.createRegisterFileRegister()
            address_offset = object_factory.createUnsignedLongintExpression()
            address_offset.setValue(str(first_row["ADDR"]))
            register_size = object_factory.createUnsignedPositiveIntExpression()
            register_size.setValue(str(int(first_row["stride"]) * 8))  # stride: Byte
            register.setName(str(reg_name[0]))
            register.setAddressOffset(address_offset)
            register.setSize(register_size)
            field_list = register.getField()
            for field in fields:
                field_list.add(field)
            registers.append(register)
    return registers
