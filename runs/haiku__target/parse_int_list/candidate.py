import re

_ITEM = re.compile(r"[+-]?[0-9]+")


def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    out = []
    for item in s.split(","):
        item = item.strip(" ")
        if not item:
            continue
        if _ITEM.fullmatch(item) is None:
            raise ValueError("bad item")
        out.append(int(item))
    return out
