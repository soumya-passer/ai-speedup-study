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
        sign = -1 if item[0] == "-" else 1
        body = item[1:] if item[0] in "+-" else item
        if not body.isascii() or not body.isdigit():
            raise ValueError("bad item")
        if len(body) <= 1000:
            append(sign * int(body))
        else:
            # int() refuses very long digit strings in newer Python; convert in chunks.
            value = 0
            for k in range(0, len(body), 1000):
                chunk = body[k:k + 1000]
                value = value * 10 ** len(chunk) + int(chunk)
            append(sign * value)
    return out
