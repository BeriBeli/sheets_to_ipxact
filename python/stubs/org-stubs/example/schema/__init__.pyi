
import sys
if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import org.example.schema.s1685_2009
import org.example.schema.s1685_2014
import org.example.schema.s1685_2022
import typing


class __module_protocol__(Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.example.schema")``.

    s1685_2009: org.example.schema.s1685_2009.__module_protocol__
    s1685_2014: org.example.schema.s1685_2014.__module_protocol__
    s1685_2022: org.example.schema.s1685_2022.__module_protocol__
