
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import java.lang
import org.example.schema
import org.example.schema.s1685_2014
import typing



class XmlGenerator:
    def __init__(self): ...
    @staticmethod
    def generateXml(componentType: org.example.schema.s1685_2014.ComponentType, string: typing.Union[java.lang.String, str]) -> None: ...


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.example")``.

    XmlGenerator: typing.Type[XmlGenerator]
    schema: org.example.schema.__module_protocol__
