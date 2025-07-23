def get_access_value(access: str) -> str:
    match access.upper():
        case "RO":
            return "read-only"
        case (
            "RW"
            | "RC"
            | "RS"
            | "WRC"
            | "WRS"
            | "WSRC"
            | "WCRS"
            | "W1C"
            | "W1S"
            | "W1T"
            | "W0C"
            | "W0S"
            | "W0T"
            | "W1SRC"
            | "W1CRS"
            | "W0SRC"
            | "W0CRS"
        ):
            return "read-write"
        case "WO" | "WC" | "WS" | "WOC" | "WOS":
            return "write-only"
        case "W1" | "WO1":
            return "writeOnce"
        case _:
            raise KeyError


def get_modified_write_value(access: str) -> str | None:
    match access.upper():
        case "RO" | "RW" | "RC" | "RS" | "WO" | "W1" | "WO1":
            return None
        case "WRC" | "W1C" | "WCRS" | "W1CRS":
            return "oneToClear"
        case "WRS" | "W1S" | "WSRC" | "W1SRC":
            return "oneToSet"
        case "W1T":
            return "oneToToggle"
        case "W0C" | "W0CRS":
            return "zeroToClear"
        case "W0S" | "W0SRC":
            return "zeroToSet"
        case "W0T":
            return "zeroToToggle"
        case "WC" | "WOC":
            return "clear"
        case "WS" | "WOS":
            return "set"
        case _:
            raise KeyError


def get_read_action_value(access: str) -> str | None:
    match access.upper():
        case (
            "RO"
            | "RW"
            | "WC"
            | "WS"
            | "W1C"
            | "W1S"
            | "W1T"
            | "W0C"
            | "W0S"
            | "W0T"
            | "WO"
            | "WOC"
            | "WOS"
            | "W1"
            | "WO1"
        ):
            return None
        case "RC" | "WRC" | "WSRC" | "W1SRC" | "W0SRC":
            return "clear"
        case "RS" | "WRS" | "WCRS" | "W1CRS" | "W0CRS":
            return "set"
        case _:
            raise KeyError
