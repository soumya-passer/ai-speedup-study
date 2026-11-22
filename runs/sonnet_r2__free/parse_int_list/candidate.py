def _slow(t):
    value = 0
    for ch in t:
        value = value * 10 + (ord(ch) - 48)
    return value


def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    out = []
    append = out.append
    for item in s.split(","):
        t = item.strip(" ")
        if not t:
            continue
        body = t[1:] if t[0] in "+-" else t
        if not (body.isascii() and body.isdigit()):
            raise ValueError("bad item")
        try:
            append(int(t))
        except ValueError:
            # int() digit-limit for very long numbers
            v = _slow(body)
            append(-v if t[0] == "-" else v)
    return out
