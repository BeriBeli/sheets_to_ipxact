from typing import Literal

from pydantic import BaseModel, Field

type AccessType = Literal[
    "read-only",
    "write-only",
    "read-write",
    "writeOnce",
    "read-writeOnce",
]

type BankAlignmentType = Literal[
    "serial",
    "parallel",
]

type EnumeratedValueUsageType = Literal[
    "read",
    "write",
    "read-write",
]

type ModifiedWriteValueType = Literal[
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

type ReadActionType = Literal[
    "clear",
    "set",
    "modify",
]

type SharedType = Literal[
    "yes",
    "no",
    "undefined",
]

type TestableTestConstraintType = Literal[
    "unconstrained",
    "restore",
    "writeAsRead",
    "readOnly",
]

type UsageType = Literal[
    "memory",
    "register",
    "reserved",
]

type FormatType = Literal[
    "bit",
    "byte",
    "shortint",
    "int",
    "longint",
    "shortreal",
    "real",
    "string",
]

type SignType = Literal[
    "signed",
    "unsigned",
]


type ParameterPrefixType = Literal[
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

type ParameterUnitType = Literal[
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


type ParameterResolveType = Literal[
    "immediate",
    "user",
    "generated",
]


class NameBaseModel(BaseModel):
    name: str = Field(
        ...,
        serialization_alias="name",
    )
    display_name: str | None = Field(
        None,
        serialization_alias="displayName",
    )
    description: str | None = Field(
        None,
        serialization_alias="description",
    )


class VendorBaseModel(BaseModel):
    vendor_extensions: list[object] | None = Field(
        None,
        serialization_alias="vendorExtensions",
    )


class IdBaseModel(BaseModel):
    id: int | str | None = Field(
        None,
        serialization_alias="@id",
    )


class SchemaBaseModel(NameBaseModel, VendorBaseModel, IdBaseModel):
    pass


class Testable(BaseModel):
    test_constraint: TestableTestConstraintType = Field(
        ...,
        serialization_alias="@testConstraint",
    )
    value: bool = Field(
        ...,
        serialization_alias="#text",
    )


class EnumeratedValue(SchemaBaseModel):
    value: int | str = Field(
        ...,
        serialization_alias="value",
    )
    usage: EnumeratedValueUsageType | None = Field(
        None,
        serialization_alias="@usage",
    )


class EnumeratedValues(BaseModel):
    enumerated_value: list[EnumeratedValue] = Field(
        [],
        serialization_alias="enumeratedValue",
    )


class Reset(IdBaseModel):
    value: int | str = Field(
        ...,
        serialization_alias="value",
    )
    mask: int | str | None = Field(
        None,
        serialization_alias="mask",
    )
    reset_type_ref: str | None = Field(
        None,
        serialization_alias="@resetTypeRef",
    )


class Resets(BaseModel):
    reset: list[Reset] = Field(
        [],
        serialization_alias="reset",
    )


class Dim(IdBaseModel):
    value: int | str = Field(
        ...,
        serialization_alias="#text",
    )


class WriteValueConstraintType(BaseModel):
    write_as_read: bool | None = Field(
        None,
        serialization_alias="writeAsRead",
    )
    use_enumerated_values: bool | None = Field(
        None,
        serialization_alias="useEnumeratedValues",
    )
    minimum: int | str | None = Field(
        None,
        serialization_alias="minimum",
    )
    maximum: int | str | None = Field(
        None,
        serialization_alias="maximum",
    )


class ViewRef(IdBaseModel):
    value: str = Field(
        ...,
        serialization_alias="#text",
    )


class Indices(BaseModel):
    index: list[int | str] = Field(
        [],
        serialization_alias="index",
    )


class PathSegmentType(IdBaseModel):
    path_segment_name: str = Field(
        ...,
        serialization_alias="pathSegmentName",
    )
    indices: Indices | None = Field(
        None,
        serialization_alias="indices",
    )


class PathSegments(BaseModel):
    path_segment: list[PathSegmentType] = Field(
        [],
        serialization_alias="pathSegment",
    )


class AccessHandle(IdBaseModel):
    view_ref: list[ViewRef] = Field(
        [],
        serialization_alias="viewRef",
    )
    indices: Indices | None = Field(
        None,
        serialization_alias="indices",
    )
    path_segments: PathSegments = Field(
        ...,
        serialization_alias="pathSegments",
    )


class AccessHandles(BaseModel):
    access_handle: list[AccessHandle] = Field(
        [],
        serialization_alias="accessHandle",
    )


class Vector(BaseModel):
    left: int | str = Field(
        ...,
        serialization_alias="left",
    )
    right: int | str = Field(
        ...,
        serialization_alias="right",
    )


class Vectors(BaseModel):
    vector: list[Vector] = Field(
        [],
        serialization_alias="vector",
    )


class Array(Vector, IdBaseModel):
    pass


class Arrays(BaseModel):
    array: list[Array] = Field(
        [],
        serialization_alias="array",
    )


class Parameter(NameBaseModel, VendorBaseModel):
    vectors: Vectors | None = Field(
        None,
    )
    arrays: Arrays | None = Field(None, serialization_alias="arrays")
    value: int | str = Field(..., serialization_alias="value")
    parameter_id: str | None = Field(
        None,
        serialization_alias="@parameterId",
    )
    prompt: str | None = Field(
        None,
        serialization_alias="@prompt",
    )
    choice_ref: str | None = Field(
        None,
        serialization_alias="@choiceRef",
    )
    order: float | None = Field(
        None,
        serialization_alias="@order",
    )
    config_groups: list[str] = Field(
        [],
        serialization_alias="@configGroups",
    )
    minimum: str | None = Field(
        None,
        serialization_alias="@minimum",
    )
    maximum: str | None = Field(
        None,
        serialization_alias="@maximum",
    )
    type_value: FormatType = Field(
        ...,
        serialization_alias="@type",
    )
    sign: SignType | None = Field(
        None,
        serialization_alias="@sign",
    )
    prefix: ParameterPrefixType | None = Field(None, serialization_alias="@prefix")
    unit: ParameterUnitType | None = Field(None, serialization_alias="@unit")
    resolve: ParameterResolveType = Field(
        ...,
        serialization_alias="@resolve",
    )


class Parameters(BaseModel):
    parameter: list[Parameter] = Field([], serialization_alias="parameter")


class FieldType(SchemaBaseModel):
    access_handles: AccessHandles | None = Field(
        None,
        serialization_alias="accessHandles",
    )
    is_present: str | None = Field(
        None,
        serialization_alias="str",
    )
    bit_offset: int | str = Field(
        ...,
        serialization_alias="bitOffset",
    )
    resets: Resets | None = Field(
        None,
        serialization_alias="resets",
    )
    type_identifier: str | None = Field(
        None,
        serialization_alias="typeIdentifier",
    )
    bit_width: int | str = Field(
        ...,
        serialization_alias="bitWidth",
    )
    volatile: bool | None = Field(None, serialization_alias="volatile")
    access: AccessType | None = Field(
        None,
        serialization_alias="access",
    )
    enumerated_values: EnumeratedValues | None = Field(
        None,
        serialization_alias="enumeratedValues",
    )
    modified_write_value: ModifiedWriteValueType | None = Field(
        None,
        serialization_alias="modifiedWriteValue",
    )
    write_value_constraint: WriteValueConstraintType | None = Field(
        None,
        serialization_alias="writeValueConstraint",
    )
    read_action: ReadActionType | None = Field(
        None,
        serialization_alias="readAction",
    )
    testable: Testable | None = Field(
        None,
        serialization_alias="testable",
    )
    reserved: int | str | None = Field(
        None,
        serialization_alias="reserved",
    )
    parameters: Parameters | None = Field(
        None,
        serialization_alias="parameters",
    )
    field_id: str | None = Field(
        None,
        serialization_alias="@fieldID",
    )


class AlternateGroup(IdBaseModel):
    value: str = Field(
        ...,
        serialization_alias="#text",
    )


class AlternateGroups(IdBaseModel):
    alternate_group: list[AlternateGroup] = Field(
        [],
        serialization_alias="alternateGroup",
    )


class AlternateRegister(SchemaBaseModel):
    access_handles: AccessHandles | None = Field(
        None,
        serialization_alias="accessHandles",
    )
    is_present: str | None = Field(
        None,
        serialization_alias="str",
    )
    alternate_groups: AlternateGroups = Field(
        ...,
        serialization_alias="alternateGroups",
    )
    type_identifier: str | None = Field(
        None,
        serialization_alias="typeIdentifier",
    )
    volatile: bool | None = Field(
        None,
        serialization_alias="volatile",
    )
    access: AccessType | None = Field(
        None,
        serialization_alias="access",
    )
    fields: list[FieldType] = Field(
        [],
        serialization_alias="field",
    )
    parameters: Parameters | None = Field(None, serialization_alias="parameters")


class AlternateRegisters(BaseModel):
    alternate_register: list[AlternateRegister] = Field(
        [],
        serialization_alias="alternateRegister",
    )


class Register(SchemaBaseModel):
    access_handles: AccessHandles | None = Field(
        None,
        serialization_alias="accessHandles",
    )
    is_present: str | None = Field(
        None,
        serialization_alias="str",
    )
    dim: list[Dim] | None = Field(
        None,
        serialization_alias="dim",
    )
    address_offset: int | str = Field(
        ...,
        serialization_alias="addressOffset",
    )
    type_identifier: str | None = Field(
        None,
        serialization_alias="typeIdentifier",
    )
    size: int | str = Field(..., serialization_alias="size")
    volatile: bool | None = Field(
        None,
        serialization_alias="volatile",
    )
    access: AccessType | None = Field(
        None,
        serialization_alias="access",
    )
    fields: list[FieldType] = Field(
        [],
        serialization_alias="field",
    )
    alternate_registers: AlternateRegisters | None = Field(
        None,
        serialization_alias="alternateRegisters",
    )
    parameters: Parameters | None = Field(
        None,
        serialization_alias="parameters",
    )


class AddressBlock(SchemaBaseModel):
    access_handles: AccessHandles | None = Field(
        None,
        serialization_alias="accessHandles",
    )
    is_present: str | None = Field(
        None,
        serialization_alias="str",
    )
    base_address: int | str = Field(
        ...,
        serialization_alias="baseAddress",
    )
    type_identifier: str | None = Field(
        None,
        serialization_alias="typeIdentifier",
    )
    range: int | str = Field(
        ...,
        serialization_alias="range",
    )
    width: int | str = Field(
        ...,
        serialization_alias="width",
    )
    usage: UsageType | None = Field(
        None,
        serialization_alias="usage",
    )
    volatile: bool | None = Field(None, serialization_alias="volatile")
    access: AccessType | None = Field(
        None,
        serialization_alias="access",
    )
    parameters: Parameters | None = Field(None, serialization_alias="parameters")
    registers: list[Register] = Field(
        [],
        serialization_alias="register",
    )
    # register_file: list[RegisterFile] = Field(
    #     [],
    #     serialization_alias="registerFile",
    # )


class MemoryMap(SchemaBaseModel):
    is_present: str | None = Field(
        None,
        serialization_alias="str",
    )
    address_block: list[AddressBlock] = Field(
        [],
        serialization_alias="addressBlock",
    )
    # bank: list[Bank] = Field(
    #     [],
    #     serialization_alias="bank",
    # )
    # subspace_map: list[SubspaceRefType] = Field(
    #     [],
    #     serialization_alias="subspaceMap",
    # )
    # memory_remap: list[MemoryRemapType] = Field(
    #     [],
    #     serialization_alias="memoryRemap",
    # )
    # address_unit_bits: AddressUnitBits | None = Field(
    #     None,
    #     serialization_alias="addressUnitBits",
    # )
    shared: SharedType | None = Field(
        None,
        serialization_alias="shared",
    )


class MemoryMaps(BaseModel):
    memory_map: list[MemoryMap] = Field(
        [],
        serialization_alias="memoryMap",
    )


class Component(BaseModel):
    vendor: str = Field(
        ...,
        serialization_alias="vendor",
    )
    library: str = Field(
        ...,
        serialization_alias="library",
    )
    name: str = Field(
        ...,
        serialization_alias="name",
    )
    version: str = Field(
        ...,
        serialization_alias="version",
    )
    memory_maps: MemoryMaps = Field(
        ...,
        serialization_alias="memoryMaps",
    )
