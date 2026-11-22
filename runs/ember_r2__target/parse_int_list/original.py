def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    out = []
    for item in s.split(","):
        i, j = 0, len(item)
        while i < j and item[i] == " ":
            i += 1
        while j > i and item[j - 1] == " ":
            j -= 1
        if i == j:
            continue
        sign = 1
        if item[i] in "+-":
            if item[i] == "-":
                sign = -1
            i += 1
        if i == j:
            raise ValueError("bad item")
        value = 0
        while i < j:
            ch = item[i]
            if ch not in "0123456789":
                raise ValueError("bad item")
            value = value * 10 + (ord(ch) - 48)
            i += 1
        out.append(sign * value)
    return out
