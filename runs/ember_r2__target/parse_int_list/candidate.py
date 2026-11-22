def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    # Fast path: int() in C via map() matches the spec except for
    # inputs that int() *accepts* but the spec rejects:
    #   * underscores ("1_0"),
    #   * whitespace other than " " ("\t", "\n", "\r", "\v", "\f",
    #     "\x1c"-"\x1f") around an item,
    #   * non-ASCII (Unicode digits / whitespace).
    # If none of those are present, int() acceptance on the allowed
    # character set is exactly the spec (except empty items and
    # >4300-digit numbers, where int() raises ValueError and we
    # fall through to the exact parser below).
    if (
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
    ):
        try:
            return list(map(int, s.split(",")))
        except ValueError:
            pass  # empty item, invalid item, or huge int: use exact parser

    # Exact reference parser (also used for non-ASCII / tab / underscore
    # inputs, huge integers, and empty items).
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
