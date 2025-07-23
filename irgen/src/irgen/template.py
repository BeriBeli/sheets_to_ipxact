import logging
from pathlib import Path

import polars as pl
from xlsxwriter import Workbook


def generate_template():
    if Path("template.xlsx").exists():
        logging.warning("Template file already exists.")
        # raise FileExistsError("Template file already exists.")

    vendor_df = pl.DataFrame(
        {
            "TAG": ["VENDOR", "LIBRARY", "NAME", "VERSION", "DESCRIPTION"],
            "VALUE": ["", "", "", "", ""]
        }
    )
    address_map_df = pl.DataFrame(
        {
            "BLOCK": [""],
            "OFFSET": [""],
            "RANGE": [""],
            "DESCRIPTION": [""]
        }
    )
    register_df = pl.DataFrame(
        {
            "ADDR": [""],
            "REG": [""],
            "FIELD": [""],
            "BIT": [""],
            "WIDTH": [""],
            "ATTRIBUTE": [""],
            "DEFAULT": [""],
            "DESCRIPTION": [""]
        }
    )
    try:
        with Workbook("template.xlsx") as wb:
            vendor_df.write_excel(workbook=wb, worksheet="vendor")
            address_map_df.write_excel(workbook=wb, worksheet="address_map")
            register_df.write_excel(workbook=wb, worksheet="register_template")
    except Exception as e:
        logging.error(f"Failed to write templates: {e}")