import logging

from lxml import etree

from utils.schema import Component


def validate_xml(xml_path, xsd_dir):
    xml_file = etree.parse(xml_path)
    parser = etree.XMLParser(resolve_entities=True, no_network=True)

    # load XSD file schema
    xsd_path = f"{xsd_dir}/index.xsd"
    schema = etree.XMLSchema(etree.parse(xsd_path, parser=parser))

    # verification
    schema.assertValid(xml_file)
    logging.info("XML validation successful.")


def generate_and_validate_ipxact(
    component: Component, output_path: str
):
    """Generates and validates the IP-XACT XML file."""
    logging.info(f"Generating IP-XACT XML file at '{output_path}'...")
    try:
        xml_output = component.to_xml(
            skip_empty=True,
            exclude_none=True,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
        )
        with open(output_path, "wb") as f:
            f.write(xml_output)
        logging.info(f"Successfully wrote XML to '{output_path}'.")

        validate_xml(output_path, "1685-2014") # TODO
    except Exception as e:
        logging.critical(f"Failed to create or validate XML file: {e}")
