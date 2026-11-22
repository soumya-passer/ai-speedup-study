def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    out = []
    append = out.append
    for item in s.split(","):
        item = item.strip(" ")
        if not item:
            continue
        body = item[1:] if item[0] in "+-" else item
        if not (body.isdigit() and body.isascii()):
            raise ValueError("bad item")
        append(int(item))
    return out
