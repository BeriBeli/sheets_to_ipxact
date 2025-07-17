import re
import logging

import polars as pl

from utils.schema import (
    FieldType,
    Register,
    AddressBlock,
    MemoryMaps,
    Component,
    Resets,
    Reset,
)
from utils.attribute import (
    get_access_value,
    get_modified_write_value,
    get_read_action_value,
)


def parse_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    df0 = df.with_columns(
        header_reg=pl.first("REG").over("ADDR"),
        start_addr_str=pl.first("ADDR").over("ADDR"),
        stride=(
            pl.col("WIDTH")
            .filter(pl.col("FIELD").is_not_null() & (pl.col("FIELD") != ""))
            .sum()
            .over("ADDR")
            // 8
        ),
    ).with_columns(
        is_expandable=pl.col("header_reg").str.contains(r"\{n\}"),
        base_reg_name=pl.coalesce(
            pl.col("header_reg").str.extract(r"(.*?)\{n\}"), pl.lit("")
        ),
        n_start=pl.col("header_reg").str.extract(r"n\s*=\s*(\d+)", 1).cast(pl.Int64),
        n_end=pl.col("header_reg").str.extract(r"~\s*(\d+)", 1).cast(pl.Int64),
        start_addr_int=pl.col("start_addr_str")
        .str.extract(r"0x([0-9a-fA-F]+)")
        .str.to_integer(base=16, strict=True),
    )
    logging.debug(df0)

    df1 = (
        df0.with_columns(
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
    )
    logging.debug(df1)

    df2 = df1.with_columns(
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

    parsed_df = df2.select(
        "ADDR", "REG", "FIELD", "BIT", "WIDTH", "ATTRIBUTE", "DEFAULT", "DESCRIPTION"
    )

    return parsed_df


def process_vendor_sheet(df: pl.DataFrame) -> Component | None:
    """Process the Sheet<vendor> to create an IP-XACT Component object"""
    try:

        def get_tag_value(tag: str) -> str:
            value = df.filter(pl.col("TAG") == tag)["VALUE"]
            if value.is_empty():
                raise ValueError(f"Tag '{tag}' not found in the Sheet<vendor> ")
            return str(value[0])

        return Component(
            vendor=get_tag_value("VENDOR"),
            library=get_tag_value("LIBRARY"),
            name=get_tag_value("NAME"),
            version=get_tag_value("VERSION"),
            memory_maps=MemoryMaps(memory_map=[]),
        )
    except (pl.exceptions.PolarsError, ValueError, KeyError) as e:
        logging.error(f"Failed to process the Sheet<vendor>: {e}")
        return None
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while processing the Sheet<vendor>: {e}"
        )
        return None


def process_address_map_sheet(df: pl.DataFrame) -> list[AddressBlock]:
    """Process the Sheet<address_map> to create a list of IP-XACT AddressBlock objects."""
    address_blocks = []
    for row in df.iter_rows(named=True):
        try:
            address_blocks.append(
                AddressBlock(
                    name=str(row["BLOCK"]),
                    base_address=str(row["OFFSET"]),
                    range=str(row["RANGE"]),
                    width=32,
                    registers=[],
                )
            )
        except KeyError as e:
            logging.error(
                f"Missing expected column in address_map sheet: {e}. Skipping row: {row}"
            )
    return address_blocks


def process_register_sheet(df: pl.DataFrame) -> list[Register]:
    """Process a single register block sheet into a list of Register objects."""
    try:
        # Pre-process the dataframe
        filled_df = df.select(pl.all().forward_fill())
        parsed_df = parse_dataframe(filled_df)
    except pl.exceptions.PolarsError as e:
        logging.error(f"Polars error during pre-processing of a register sheet: {e}")
        return []

    registers = []
    # Group by register to process all its fields together
    for reg_name, group in parsed_df.group_by("REG", maintain_order=True):
        if not reg_name:
            logging.warning("Skipping rows with no register name.")
            continue

        fields: list[FieldType] = []
        total_bit_width = 0
        first_row = group.row(0, named=True)

        for field_row in group.iter_rows(named=True):
            try:
                bit_match = re.findall(r"\[(?:\d+:)?(\d+)]", str(field_row["BIT"]))
                if not bit_match:
                    raise ValueError(
                        f"Could not parse bit offset from '{field_row['BIT']}"
                    )

                field = FieldType(
                    name=str(field_row["FIELD"]),
                    description=None,  # str(field_row.get("DESCRIPTION"))
                    bit_offset=int(bit_match[0]),
                    bit_width=str(field_row["WIDTH"]),
                    access=get_access_value(str(field_row["ATTRIBUTE"])),
                    modified_write_value=get_modified_write_value(
                        str(field_row["ATTRIBUTE"])
                    ),
                    read_action=get_read_action_value(str(field_row["ATTRIBUTE"])),
                    resets=Resets(reset=[Reset(value=str(field_row["DEFAULT"]))]),
                )
                fields.append(field)
                total_bit_width += int(field.bit_width)
            except (KeyError, ValueError, TypeError) as e:
                logging.error(
                    f"Skipping invalid field '{field_row.get('FIELD', 'N/A')}' in register '{reg_name}': {e}"
                )

        if fields:
            # skip reserved field
            fields = [
                field
                for field in fields
                if not re.match(r"^(rsvd|reserved)\d*$", field.name.lower())
            ]

            registers.append(
                Register(
                    name=str(reg_name[0]),
                    address_offset=str(first_row["ADDR"]),
                    size=total_bit_width,
                    fields=fields,
                )
            )
    return registers
