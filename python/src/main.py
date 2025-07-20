import sys
import glob
import logging
import argparse
from typing import Any

import polars as pl
import fastexcel
import jpype

from utils.parser import (
    process_vendor_sheet,
    process_address_map_sheet,
    process_register_sheet,
)

# configuration constrants
DEBUG = False
LOG_FILE = "debug.log"
DEFAULT_EXCEL_NAME = "example.xlsx"
DEFAULT_VENDOR_SHEET = "version"
DEFAULT_ADDRESS_SHEET = "address_map"
DEFAULT_OUTPUT_XML = "example.xml"
DEFAULT_IPXACT_VERSION = "1685-2014"
DEFAULT_JAVA_JAR = "../java/target/ipxact_schema-1.0.0.jar"
DEFAULT_JAVA_DEPENDENCY_JARS = "../java/target/dependency/*.jar"


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
        default=DEFAULT_EXCEL_NAME,
        help="Path to the input Excel file",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_XML,
        help="Path for the output XML file.",
    )
    parser.add_argument(
        "--vendor_sheet",
        default=DEFAULT_VENDOR_SHEET,
        help="Name of the vendor sheet.",
    )
    parser.add_argument(
        "--address_sheet",
        default=DEFAULT_ADDRESS_SHEET,
        help="Name of the address map sheet.",
    )
    parser.add_argument(
        "--ipxact_version",
        default=DEFAULT_IPXACT_VERSION,
        help="IP-XACT version to use (e.g., 1685-2009, 1685-2014, 1685-2022)",
    )
    return parser


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    setup_logging(args.debug)

    excel_name = str(args.excel)
    xml_path = str(args.output)
    vendor_sheet = str(args.vendor_sheet)
    address_sheet = str(args.address_sheet)
    ipxact_version = str(args.ipxact_version)
    if ipxact_version != DEFAULT_IPXACT_VERSION:
        logging.critical(
            f"IP-XACT version '{ipxact_version}' is not supported now."
        )
        sys.exit(1)


    try:
        sheet_names = fastexcel.read_excel(excel_name).sheet_names
    except (fastexcel.FastExcelError, FileNotFoundError) as e:
        logging.critical(f"Could not read Excel file '{excel_name}': {e}")
        sys.exit(1)

    try:
        project_jar = DEFAULT_JAVA_JAR
        dependency_jars = glob.glob(DEFAULT_JAVA_DEPENDENCY_JARS)

        classpath = [project_jar] + dependency_jars

        logging.info("Starting JVM...")
        jpype.startJVM(classpath=classpath)
        logging.info("JVM Started.")

        # import Java classes
        ObjectFactory = jpype.JClass("org.example.schema.s1685_2014.ObjectFactory")
        XmlGenerator = jpype.JClass("org.example.XmlGenerator")

        logging.info("Java classes imported successfully.")

        object_factory = ObjectFactory()
        match (ipxact_version):
            case "1685-2009":    
                AccessType = jpype.JClass("org.example.schema.s1685_2009.AccessType")
                ModifiedWriteValueType = jpype.JClass("org.example.schema.s1685_2009.ModifiedWriteValueType")
                ReadActionType = jpype.JClass("org.example.schema.s1685_2009.ReadActionType")
            case "1685-2014":
                AccessType = jpype.JClass("org.example.schema.s1685_2014.AccessType")
                ModifiedWriteValueType = jpype.JClass("org.example.schema.s1685_2014.ModifiedWriteValueType")
                ReadActionType = jpype.JClass("org.example.schema.s1685_2014.ReadActionType")
            case "1685-2022":
                AccessType = jpype.JClass("org.example.schema.s1685_2022.AccessType")
                ModifiedWriteValueType = jpype.JClass("org.example.schema.s1685_2022.ModifiedWriteValueType")
                ReadActionType = jpype.JClass("org.example.schema.s1685_2022.ReadActionType")
            case _:
                logging.error(f"Unsupported IP-XACT version: {ipxact_version}")
        IpXactVersion = jpype.JClass("org.example.IpXactVersion")

        address_blocks: list[Any] = []
        all_registers: dict[str, list[Any]] = {}

        logging.info(f"Processing sheets: {sheet_names}")
        for sheet_name in sheet_names:
            logging.info(f"--- Reading sheet: {sheet_name} ---")
            try:
                df = pl.read_excel(excel_name, sheet_name=sheet_name)
            except Exception as e:
                logging.error(f"Could not read sheet '{sheet_name}' with Polars: {e}")
                continue

            if sheet_name == vendor_sheet:
                component = process_vendor_sheet(df, object_factory)
            elif sheet_name == address_sheet:
                address_blocks = process_address_map_sheet(df, object_factory)
            else:
                all_registers[sheet_name] = process_register_sheet(
                    df, object_factory, AccessType, ModifiedWriteValueType, ReadActionType
                )

        if not component:
            logging.critical("Failed to parse vendor information. Aborting.")
            sys.exit(1)
        if not address_blocks:
            logging.critical("Failed to parse address blocks. Aborting.")
            sys.exit(1)

        # Assemble the final component data structure
        logging.info("Assembling final component structure...")
        for block in address_blocks:
            if block.getName() in all_registers:
                register_list = block.getRegisterData()
                for reg in all_registers[block.getName()]:
                    register_list.add(reg)
                logging.info(
                    f"Mapped {len(register_list)} registers to address block '{block.getName()}'."
                )
            else:
                logging.warning(
                    f"No register block sheet found for address block '{block.getName()}'."
                )

        memory_map = object_factory.createMemoryMapType()
        memory_map.setName(component.getName())
        address_block_list = memory_map.getMemoryMap()
        for block in address_blocks:
            address_block_list.add(block)
        memory_maps = object_factory.createMemoryMaps()
        memory_map_list = memory_maps.getMemoryMap()
        memory_map_list.add(memory_map)
        component.setMemoryMaps(memory_maps)

        XmlGenerator.generateXml(component, IpXactVersion.fromValue(ipxact_version), xml_path)

    except Exception as e:
        logging.critical(f"An error occurred during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
