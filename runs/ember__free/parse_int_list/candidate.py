def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    # Fast path: int() (C implementation, via map in C) is exactly
    # equivalent to the spec provided the input contains only ASCII
    # and none of the characters that int() additionally accepts:
    #   '_' (digit grouping), and ASCII whitespace other than ' '
    #   (\t \n \r \v \f \x1c-\x1f).  Non-ASCII input is rejected here
    #   too, which excludes Unicode digits / Unicode whitespace that
    #   int() would accept.  Anything else falls back to the exact
    #   reference parser below.
    try:
        clean = (
            s.isascii()
            and "_" not in s
            and "\t" not in s
            and "\n" not in s
            and "\r" not in s
            and "\v" not in s
            and "\f" not in s
            and "\x1c" not in s
            and "\x1d" not in s
            and "\x1e" not in s
            and "\x1f" not in s
        )
    except (AttributeError, TypeError):
        clean = False
    if clean:
        try:
            # No empty / space-only items: the common (benchmark) case.
            return list(map(int, s.split(",")))
        except ValueError:
            try:
                # Empty / space-only items must be skipped.  This also
                # raises ValueError for genuinely bad items.
                return [int(item) for item in s.split(",") if item.strip(" ")]
            except ValueError:
                # Either a genuinely bad item (reference parser will
                # raise the same) or an integer with >4300 digits,
                # which int() refuses but the reference parser accepts.
                pass
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
