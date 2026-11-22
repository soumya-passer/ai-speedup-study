def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    out = []
    append = out.append
    _int = int
    for item in s.split(','):
        t = item.strip(' ')
        if not t:
            continue
        c = t[0]
        if c == '-' or c == '+':
            u = t[1:]
            if not u.isdigit() or not u.isascii():
                raise ValueError("bad item")
            append(_int(t))
        else:
            if not t.isdigit() or not t.isascii():
                raise ValueError("bad item")
            append(_int(t))
    return out
