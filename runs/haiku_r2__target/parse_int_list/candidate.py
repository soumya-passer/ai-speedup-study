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
        sign = item[0]
        if sign == "+" or sign == "-":
            body = item[1:]
        else:
            body = item
            sign = ""
        if not body or not (body.isascii() and body.isdigit()):
            raise ValueError("bad item")
        if len(body) > 18:
            # Long digit runs: loop like the original so there is no int() digit limit.
            value = 0
            for ch in body:
                value = value * 10 + (ord(ch) - 48)
        else:
            value = int(body)
        append(-value if sign == "-" else value)
    return out
