from typing import Literal

from pydantic_xml import BaseXmlModel, element, attr


NAMESPACE = "ipxact"

NAMESPACE_MAP = {
    "ipxact": "http://www.accellera.org/XMLSchema/IPXACT/1685-2014",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

SCHEMA_LOCATION = (
    "http://www.accellera.org/XMLSchema/IPXACT/1685-2014 "
    "http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd"
)

AccessType = Literal[
    "read-only",
    "write-only",
    "read-write",
    "writeOnce",
    "read-writeOnce",
]

BankAlignmentType = Literal[
    "serial",
    "parallel",
]

EnumeratedValueUsageType = Literal[
    "read",
    "write",
    "read-write",
]

ModifiedWriteValueType = Literal[
    "oneToClear",
    "oneToSet",
    "oneToToggle",
    "zeroToClear",
    "zeroToSet",
    "zeroToToggle",
    "clear",
    "set",
    "modify",
]

ReadActionType = Literal[
    "clear",
    "set",
    "modify",
]

SharedType = Literal[
    "yes",
    "no",
    "undefined",
]

TestableTestConstraintType = Literal[
    "unconstrained",
    "restore",
    "writeAsRead",
    "readOnly",
]

UsageType = Literal[
    "memory",
    "register",
    "reserved",
]

FormatType = Literal[
    "bit",
    "byte",
    "shortint",
    "int",
    "longint",
    "shortreal",
    "real",
    "string",
]

SignType = Literal[
    "signed",
    "unsigned",
]


ParameterPrefixType = Literal[
    "deca",
    "hecto",
    "kilo",
    "mega",
    "giga",
    "tera",
    "peta",
    "exa",
    "zetta",
    "yotta",
    "deci",
    "centi",
    "milli",
    "micro",
    "nano",
    "pico",
    "femto",
    "atto",
    "zepto",
    "yocto",
]

ParameterUnitType = Literal[
    "second",
    "ampere",
    "kelvin",
    "hertz",
    "joule",
    "watt",
    "coulomb",
    "volt",
    "farad",
    "ohm",
    "siemens",
    "henry",
    "Celsius",
]


ParameterResolveType = Literal[
    "immediate",
    "user",
    "generated",
]


class SchemaBaseModel(BaseXmlModel, ns=NAMESPACE, nsmap=NAMESPACE_MAP):
    pass


class NameBaseModel(SchemaBaseModel):
    name: str = element(
        tag="name",
    )
    display_name: str | None = element(
        tag="displayName",
        default=None,
    )
    description: str | None = element(
        tag="description",
        default=None,
    )


class VendorBaseModel(SchemaBaseModel):
    vendor_extensions: list[str] | None = element(
        tag="vendorExtensions",
        default=None,
    )


class IdBaseModel(SchemaBaseModel):
    id: int | str | None = attr(
        name="id",
        default=None,
    )


class Testable(SchemaBaseModel):
    test_constraint: TestableTestConstraintType = attr(
        name="testConstraint",
    )
    content: bool


class EnumeratedValue(NameBaseModel, VendorBaseModel, IdBaseModel):
    value: int | str = element(
        tag="value",
    )
    usage: EnumeratedValueUsageType | None = attr(
        name="usage",
        default=None,
    )


class EnumeratedValues(SchemaBaseModel):
    enumerated_value: list[EnumeratedValue] = element(
        tag="enumeratedValue",
        default=[],
    )


class Reset(IdBaseModel):
    value: int | str = element(
        tag="value",
    )
    mask: int | str | None = element(
        tag="mask",
        default=None,
    )
    reset_type_ref: str | None = attr(
        name="resetTypeRef",
        default=None,
    )


class Resets(SchemaBaseModel):
    reset: list[Reset] = element(
        tag="reset",
        default=[],
    )


class Dim(IdBaseModel):
    content: int | str


class WriteValueConstraintType(SchemaBaseModel):
    write_as_read: bool | None = element(
        tag="writeAsRead",
        default=None,
    )
    use_enumerated_values: bool | None = element(
        tag="useEnumeratedValues",
        default=None,
    )
    minimum: int | str | None = element(
        tag="minimum",
        default=None,
    )
    maximum: int | str | None = element(
        tag="maximum",
        default=None,
    )


class ViewRef(IdBaseModel):
    content: str


class Indices(SchemaBaseModel):
    index: list[int | str] = element(
        tag="index",
        default=[],
    )


class PathSegmentType(IdBaseModel):
    path_segment_name: str = element(
        tag="pathSegmentName",
    )
    indices: Indices | None = element(
        tag="indices",
        default=None,
    )


class PathSegments(SchemaBaseModel):
    path_segment: list[PathSegmentType] = element(
        tag="pathSegment",
        default=[],
    )


class AccessHandle(IdBaseModel):
    view_ref: list[ViewRef] = element(
        tag="viewRef",
        default=[],
    )
    indices: Indices | None = element(
        tag="indices",
        default=None,
    )
    path_segments: PathSegments = element(
        tag="pathSegments",
    )


class AccessHandles(SchemaBaseModel):
    access_handle: list[AccessHandle] = element(
        tag="accessHandle",
        default=[],
    )


class Vector(SchemaBaseModel):
    left: int | str = element(
        tag="left",
    )
    right: int | str = element(
        tag="right",
    )


class Vectors(SchemaBaseModel):
    vector: list[Vector] = element(
        tag="vector",
        default=[],
    )


class Array(Vector, IdBaseModel):
    pass


class Arrays(SchemaBaseModel):
    array: list[Array] = element(
        tag="array",
        default=[],
    )


class Parameter(NameBaseModel, VendorBaseModel):
    vectors: Vectors | None = element(
        default=None,
    )
    arrays: Arrays | None = element(
        tag="arrays",
        default=None,
    )
    value: int | str = element(
        tag="value",
    )
    parameter_id: str | None = attr(
        name="parameterId",
        default=None,
    )
    prompt: str | None = attr(
        name="prompt",
        default=None,
    )
    choice_ref: str | None = attr(
        name="choiceRef",
        default=None,
    )
    order: float | None = attr(
        name="order",
        default=None,
    )
    # config_groups: list[str] | None
    minimum: str | None = attr(
        name="minimum",
        default=None,
    )
    maximum: str | None = attr(
        name="maximum",
        default=None,
    )
    type_value: FormatType = attr(
        name="type",
    )
    sign: SignType | None = attr(
        name="sign",
        default=None,
    )
    prefix: ParameterPrefixType | None = attr(
        name="prefix",
        default=None,
    )
    unit: ParameterUnitType | None = attr(
        name="unit",
        default=None,
    )
    resolve: ParameterResolveType = attr(
        name="resolve",
    )


class Parameters(SchemaBaseModel):
    parameter: list[Parameter] = element(
        tag="parameter",
        default=[],
    )


class FieldType(NameBaseModel, VendorBaseModel, IdBaseModel):
    access_handles: AccessHandles | None = element(
        tag="accessHandles",
        default=None,
    )
    is_present: str | None = element(
        tag="isPresent",
        default=None,
    )
    bit_offset: int | str = element(
        tag="bitOffset",
    )
    resets: Resets | None = element(
        tag="resets",
        default=None,
    )
    type_identifier: str | None = element(
        tag="typeIdentifier",
        default=None,
    )
    bit_width: int | str = element(
        tag="bitWidth",
    )
    volatile: bool | None = element(
        tag="volatile",
        default=None,
    )
    access: AccessType | None = element(
        tag="access",
        default=None,
    )
    enumerated_values: EnumeratedValues | None = element(
        tag="enumeratedValues",
        default=None,
    )
    modified_write_value: ModifiedWriteValueType | None = element(
        tag="modifiedWriteValue",
        default=None,
    )
    write_value_constraint: WriteValueConstraintType | None = element(
        tag="writeValueConstraint",
        default=None,
    )
    read_action: ReadActionType | None = element(
        tag="readAction",
        default=None,
    )
    testable: Testable | None = element(
        tag="testable",
        default=None,
    )
    reserved: int | str | None = element(
        tag="reserved",
        default=None,
    )
    parameters: Parameters | None = element(
        tag="parameters",
        default=None,
    )
    element_id: str | None = attr(
        name="elementID",
        default=None,
    )


class AlternateGroup(IdBaseModel):
    content: str


class AlternateGroups(IdBaseModel):
    alternate_group: list[AlternateGroup] = element(
        tag="alternateGroup",
        default=[],
    )


class AlternateRegister(NameBaseModel, VendorBaseModel, IdBaseModel):
    access_handles: AccessHandles | None = element(
        tag="accessHandles",
        default=None,
    )
    is_present: str | None = element(
        tag="isPresent",
        default=None,
    )
    alternate_groups: AlternateGroups = element(
        tag="alternateGroups",
    )
    type_identifier: str | None = element(
        tag="typeIdentifier",
        default=None,
    )
    volatile: bool | None = element(
        tag="volatile",
        default=None,
    )
    access: AccessType | None = element(
        tag="access",
        default=None,
    )
    fields: list[FieldType] = element(
        tag="field",
        default=[],
    )
    parameters: Parameters | None = element(
        tag="parameters",
        default=None,
    )


class AlternateRegisters(SchemaBaseModel):
    alternate_register: list[AlternateRegister] = element(
        tag="alternateRegister",
        default=[],
    )


class Register(NameBaseModel, VendorBaseModel, IdBaseModel):
    access_handles: AccessHandles | None = element(
        tag="accessHandles",
        default=None,
    )
    is_present: str | None = element(
        tag="isPresent",
        default=None,
    )
    dim: list[Dim] | None = element(
        tag="dim",
        default=None,
    )
    address_offset: int | str = element(
        tag="addressOffset",
    )
    type_identifier: str | None = element(
        tag="typeIdentifier",
        default=None,
    )
    size: int | str = element(
        tag="size",
    )
    volatile: bool | None = element(
        tag="volatile",
        default=None,
    )
    access: AccessType | None = element(
        tag="access",
        default=None,
    )
    fields: list[FieldType] = element(
        tag="field",
        default=[],
    )
    alternate_registers: AlternateRegisters | None = element(
        tag="alternateRegisters",
        default=None,
    )
    parameters: Parameters | None = element(
        tag="parameters",
        default=None,
    )


class AddressBlock(NameBaseModel, VendorBaseModel, IdBaseModel):
    access_handles: AccessHandles | None = element(
        tag="accessHandles",
        default=None,
    )
    is_present: str | None = element(
        tag="isPresent",
        default=None,
    )
    base_address: int | str = element(
        tag="baseAddress",
    )
    type_identifier: str | None = element(
        tag="typeIdentifier",
        default=None,
    )
    range: int | str = element(
        tag="range",
    )
    width: int | str = element(
        tag="width",
    )
    usage: UsageType | None = element(
        tag="usage",
        default=None,
    )
    volatile: bool | None = element(
        tag="volatile",
        default=None,
    )
    access: AccessType | None = element(
        tag="access",
        default=None,
    )
    parameters: Parameters | None = element(
        tag="parameters",
        default=None,
    )
    registers: list[Register] = element(
        tag="register",
        default=[],
    )
    # register_file: list[RegisterFile]


class MemoryMap(NameBaseModel, VendorBaseModel, IdBaseModel):
    is_present: str | None = element(
        tag="isPresent",
        default=None,
    )
    address_block: list[AddressBlock] = element(
        tag="addressBlock",
        default=[],
    )
    # bank: list[Bank]
    # subspace_map: list[SubspaceRefType]
    # memory_remap: list[MemoryRemapType]
    # address_unit_bits: AddressUnitBits | None
    shared: SharedType | None = element(
        tag="shared",
        default=None,
    )


class MemoryMaps(SchemaBaseModel):
    memory_map: list[MemoryMap] = element(
        tag="memoryMap",
        default=[],
    )


class Component(SchemaBaseModel, tag="component"):
    schema_location: str = attr(
        name="schemaLocation",
        default=SCHEMA_LOCATION,
        ns="xsi",
    )
    vendor: str = element(
        tag="vendor",
    )
    library: str = element(
        tag="library",
    )
    name: str = element(
        tag="name",
    )
    version: str = element(
        tag="version",
    )
    memory_maps: MemoryMaps = element(
        tag="memoryMaps",
    )
