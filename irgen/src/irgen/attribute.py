def get_access_value(access: str) -> str:
    match access:
        case "RW":
            return "read-write"
        case "RO":
            return "read-only"
        case "WO":
            return "write-only"
        case "W1C":
            return "read-write"
        case "RC":
            return "read-only"
        case _:
            raise KeyError


def get_modified_write_value(access: str) -> str | None:
    match access:
        case "RW":
            return None
        case "RO":
            return None
        case "WO":
            return None
        case "W1C":
            return "oneToClear"
        case "RC":
            return None
        case _:
            raise KeyError


def get_read_action_value(access: str) -> str | None:
    match access:
        case "RW":
            return None
        case "RO":
            return None
        case "WO":
            return None
        case "W1C":
            return None
        case "RC":
            return "clear"
        case _:
            raise KeyError
