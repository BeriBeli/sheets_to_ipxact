import re
import logging
from typing import Dict, Any

from lxml import etree

from utils.schema import Component


def create_ipxact_xml(
    component_data: Dict[str, Any],
    root_tag: str = "component",
    ns_map: Dict[str, str] | None = None,
    schema_location: str | None = None,
    additional_attrs: Dict[str, str] | None = None,
    default_ns_prefix: str | None = None,
) -> str:
    """
    Creates an IP-XACT XML document with namespaces using the lxml library.

    Args:
        component_data: The component data dictionary.
        root_tag: The tag name for the root element.
        ns_map: A dictionary for namespace mapping, e.g.,
                {'spirit': 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009'}.
        schema_location: The schema location string, e.g.,
                         "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009 http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009/index.xsd".
        additional_attrs: A dictionary of additional attributes for the root element.
        default_ns_prefix: The prefix to use for the default namespace. Elements
                           without a prefix in the data will belong to this namespace.

    Returns:
        A formatted XML string.
    """
    ns_map = ns_map or {}

    # Validate namespace parameters
    if not isinstance(ns_map, dict):
        raise TypeError("ns_map must be a dictionary")
    if default_ns_prefix and default_ns_prefix not in ns_map:
        raise ValueError(f"default_ns_prefix '{default_ns_prefix}' not found in ns_map")

    # Determine the namespace URI for unprefixed elements
    default_ns_uri = ns_map.get(default_ns_prefix)

    # Helper function to get the fully qualified tag name for lxml
    def get_qname(tag: str) -> str:
        # If a default namespace is active and the tag is not prefixed,
        # format it as {uri}tag for lxml.
        if default_ns_uri and ":" not in tag:
            return f"{{{default_ns_uri}}}{tag}"
        return tag

    # Create the root element with its namespace map
    root = etree.Element(get_qname(root_tag), nsmap=ns_map)

    # Add schema location if provided and the 'xsi' prefix is mapped
    if schema_location and "xsi" in ns_map:
        xsi_uri = ns_map["xsi"]
        # The key for a namespaced attribute must be in the format {namespace_uri}attribute_name
        location_attr_qname = f"{{{xsi_uri}}}schemaLocation"
        root.set(location_attr_qname, schema_location)

    # Add any other additional attributes
    if additional_attrs:
        for attr, value in additional_attrs.items():
            root.set(attr, value)

    def build_xml(
        parent: etree._Element, data: Any, list_item_tag: str | None = None
    ) -> None:
        """
        Recursively builds the XML tree from the data structure.

        Args:
            parent: The parent lxml element to which new elements will be appended.
            data: The data to convert into XML (dict, list, or primitive).
            list_item_tag: The tag name to use for items in a list. This is passed
                           when a list is found as a value in a dictionary.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    # If the value is a list, recurse, passing the dictionary key
                    # to be used as the tag name for each item in the list.
                    build_xml(parent, value, list_item_tag=key)
                else:
                    # Create a new sub-element and recurse into it.
                    element = etree.SubElement(parent, get_qname(key))
                    build_xml(element, value)
        elif isinstance(data, list):
            if not list_item_tag:
                # This case handles a list that isn't a value in a dictionary.
                # Each item is processed directly against the parent.
                for item in data:
                    build_xml(parent, item)
            else:
                # This is the standard case: a list as a dictionary value.
                # Create an element for each item using the provided tag from the dictionary key.
                for item in data:
                    element = etree.SubElement(parent, get_qname(list_item_tag))
                    build_xml(element, item)
        elif data is not None:
            # For simple types (string, int, etc.), set the text content of the parent element.
            parent.text = str(data)

    # Start building the XML content from the root using the component data
    build_xml(root, component_data)

    # Serialize the lxml tree to a pretty-printed string, including XML declaration
    return etree.tostring(
        root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
    ).decode("UTF-8")


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
    component: Component, output_path: str, xml_config: dict
):
    """Generates and validates the IP-XACT XML file."""
    logging.info(f"Generating IP-XACT XML file at '{output_path}'...")
    component_dict = component.model_dump(exclude_none=True, by_alias=True)
    try:
        xml_output = create_ipxact_xml(component_data=component_dict, **xml_config)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_output)
        logging.info(f"Successfully wrote XML to '{output_path}'.")

        ipxact_schema_version = re.findall(
            r"/([^/]+)/index\.xsd", xml_config.get("schema_location", "")
        )
        if not ipxact_schema_version:
            raise Exception
        validate_xml(output_path, str(ipxact_schema_version[0]))
    except Exception as e:
        logging.critical(f"Failed to create or validate XML file: {e}")
