import re as _re
import sys as _sys

try:
    _sys.set_int_max_str_digits(0)
except Exception:
    pass

_BAD = _re.compile(r'[^-0-9+, ]').search
_int = int
_map = map
_list = list

def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    if not s:
        return []
    if _BAD(s) is None:
        # Common case: only digits, '+', '-', ',' and ' '. Then int()
        # matches the spec exactly (it strips ' ' itself), so convert
        # the whole split in C with map. Blanks (",,", leading/trailing
        # comma, spaces-only item) raise here and fall through to the
        # strict loop which skips them.
        try:
            return _list(_map(_int, s.split(',')))
        except ValueError:
            pass
    out = []
    append = out.append
    for item in s.split(","):
        t = item.strip(" ")
        if not t:
            continue
        c = t[0]
        if c == "+" or c == "-":
            if len(t) == 1 or t[1:].strip("0123456789") != "":
                raise ValueError("bad item")
            append(_int(t))
        elif t.strip("0123456789") != "":
            raise ValueError("bad item")
        else:
            append(_int(t))
    return out
