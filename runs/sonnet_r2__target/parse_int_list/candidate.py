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
        if item.isascii() and (item.isdigit() or (item[0] in "+-" and item[1:].isdigit())):
            append(int(item))
        else:
            raise ValueError("bad item")
    return out
