from typing import List, Dict, Literal
from pydantic import BaseModel, Field


class SchemaObject(BaseModel):
    name: Literal["register-description-format"] = Field(...)
    version: str = Field(...)


class LinkObject(BaseModel):
    text: str = Field(...)
    href: str = Field(...)


class RootObject(BaseModel):
    desc: str | None = Field(None)
    version: str | None = Field(None)
    links: List[LinkObject] | None = Field(None)
    children: List[str] = Field(...)
    expanded: List[str] | None = Field(None)
    data_width: int | None = Field(None)
    default_reset: str | None = Field(None)


class EnumValueObject(BaseModel):
    name: str = Field(...)
    value: str = Field(...)
    doc: str = Field(...)


class ResetObject(BaseModel):
    value: str = Field(...)
    names: List[str] = Field(...)


class FieldObject(BaseModel):
    name: str = Field(...)
    nbits: int = Field(...)
    lsb: int = Field(...)
    access: str = Field(...)
    reset: ResetObject | str | None = Field(None)
    doc: str | None = Field(None)
    enum_: List[EnumValueObject] | None = Field(None)
    # experimental
    repr: str | None = Field(None)
    custom_decode: str | None = Field(None)
    custom_encode: str | None = Field(None)


class BlockElement(BaseModel):
    type_: Literal["blk"] = Field(..., alias="type")
    version: str | None = Field(None)
    id_: str = Field(..., alias="id")
    name: str = Field(...)
    desc: str | None = Field(None)
    offset: str | None = Field(None)
    links: List[LinkObject] | None = Field(None)
    size: str | None = Field(None)
    children: List[str] = Field(...)
    doc: str | None = Field(None)
    data_width: int | None = Field(None)
    default_reset: str | None = Field(None)


class RegisterElement(BaseModel):
    type_: Literal["reg"] = Field(..., alias="type")
    id_: str = Field(..., alias="id")
    name: str = Field(...)
    offset: str = Field(...)
    desc: str | None = Field(None)
    fields: List[FieldObject] | None = Field(None)
    doc: str | None = Field(None)


class MemoryElement(BaseModel):
    type_: Literal["mem"] = Field(..., alias="type")
    id_: str = Field(..., alias="id")
    name: str = Field(...)
    offset: str = Field(...)
    size: str = Field(...)
    desc: str | None = Field(None)
    doc: str | None = Field(None)


class IncludeElement(BaseModel):
    type_: Literal["include"] = Field(..., alias="type")
    id_: str = Field(..., alias="id")
    name: str = Field(...)
    offset: str | None = Field(None)
    url: str = Field(...)
    desc: str | None = Field(None)
    doc: str | None = Field(None)


class DocumentObject(BaseModel):
    schema_: SchemaObject = Field(..., alias="schema")
    root: RootObject = Field(...)
    elements: Dict[str, BlockElement | RegisterElement | MemoryElement | IncludeElement] = Field(...)
