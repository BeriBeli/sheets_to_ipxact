import sys
import logging
import tomllib
import argparse

import polars as pl
import fastexcel

from utils.schema import (
    Register,
    AddressBlock,
    MemoryMap,
    MemoryMaps,
    Component,
)
from utils.parser import (
    process_vendor_sheet,
    process_address_map_sheet,
    process_register_sheet,
)
from utils.generate import generate_and_validate_ipxact

# configuration constrants
DEBUG = False
LOG_FILE = "debug.log"
CONFIG_FILE = "config/common.toml"
DEFAULT_EXCEL_NAME = "example.xlsx"
DEFAULT_VENDOR_SHEET = "version"
DEFAULT_ADDRESS_SHEET = "address_map"
DEFAULT_OUTPUT_XML = "example.xml"


def setup_logging(debug: bool):
    """Configures logging based on the debug flag."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]\n %(message)s",
        filename=LOG_FILE,
        filemode="w",
    )
    # log to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)


def setup_arg_parser() -> argparse.ArgumentParser:
    """Set up and return the argument parser."""
    # TODO
    parser = argparse.ArgumentParser(
        description="Convert spreadsheets register maps to IP-XACT XML files."
    )
    parser.add_argument(
        "-d",
        "--debug",
        default=DEBUG,
        action="store_true",
        help="Enable debug logging.",
    )
    parser.add_argument(
        "--excel",
        default=None,
        help="Path to the input Excel file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Path for the output XML file.",
    )
    return parser


def load_config(path: str) -> dict:
    """Load configuration from a TOML file."""
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        logging.error(f"Cannot find the configuration file at '{path}'")
    except tomllib.TOMLDecodeError as e:
        logging.error(f"Error decoding the TOML configuration file '{path}': {e}")
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while reading the configuration file '{path}': {e}"
        )
    return {}


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    setup_logging(args.debug)

    config = load_config(CONFIG_FILE)
    if args.excel is None:
        excel_name = config.get("sheet_name", DEFAULT_EXCEL_NAME)
    else:
        excel_name = args.excel
    if args.output is None:
        xml_path = config.get("xml_name", DEFAULT_OUTPUT_XML)
    else:
        xml_path = args.output
    vendor_sheet = config.get("vendor_sheet", DEFAULT_VENDOR_SHEET)
    address_sheet = config.get("address_sheet", DEFAULT_ADDRESS_SHEET)

    logging.debug(config)

    try:
        sheet_names = fastexcel.read_excel(excel_name).sheet_names
    except (fastexcel.FastExcelError, FileNotFoundError) as e:
        logging.critical(f"Could not read Excel file '{excel_name}': {e}")
        sys.exit(1)

    component: Component | None = None
    address_blocks: list[AddressBlock] = []
    all_registers: dict[str, list[Register]] = {}

    logging.info(f"Processing sheets: {sheet_names}")
    for sheet_name in sheet_names:
        logging.info(f"--- Reading sheet: {sheet_name} ---")
        try:
            df = pl.read_excel(excel_name, sheet_name=sheet_name)
        except Exception as e:
            logging.error(f"Could not read sheet '{sheet_name}' with Polars: {e}")
            continue

        if sheet_name == vendor_sheet:
            component = process_vendor_sheet(df)
        elif sheet_name == address_sheet:
            address_blocks = process_address_map_sheet(df)
        else:
            all_registers[sheet_name] = process_register_sheet(df)

    if not component:
        logging.critical("Failed to parse vendor information. Aborting.")
        sys.exit(1)
    if not address_blocks:
        logging.critical("Failed to parse address blocks. Aborting.")
        sys.exit(1)

    # Assemble the final component data structure
    logging.info("Assembling final component structure...")
    for block in address_blocks:
        if block.name in all_registers:
            block.registers = all_registers[block.name]
            logging.info(
                f"Mapped {len(block.registers)} registers to address block '{block.name}'."
            )
        else:
            logging.warning(
                f"No register block sheet found for address block '{block.name}'."
            )

    memory_map = MemoryMap(name=component.name, address_block=address_blocks)
    component.memory_maps = MemoryMaps(memory_map=[memory_map])

    generate_and_validate_ipxact(component, xml_path)


if __name__ == "__main__":
    main()
