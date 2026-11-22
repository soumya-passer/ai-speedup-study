def _slow(s):
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


def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    # int() differs from the spec only for characters it treats as
    # whitespace (tabs/newlines/etc, incl. \\x1c-\\x1f), underscores
    # between digits, and non-ASCII digits/whitespace.  If any of
    # those are present, use the exact reference parser.  Otherwise
    # int() is exactly equivalent (apart from empty items and the
    # int_max_str_digits limit, both handled below).
    if not s.isascii() or '_' in s or '\t' in s or '\n' in s or '\r' in s or '\v' in s or '\f' in s or '\x1c' in s or '\x1d' in s or '\x1e' in s or '\x1f' in s:
        return _slow(s)
    parts = s.split(',')
    try:
        # Fastest path: no empty/space-only items (the common case).
        # int() in C strips spaces and validates sign+digits.
        return list(map(int, parts))
    except ValueError:
        pass
    try:
        # Empty / space-only items are skipped.
        return [int(v) for item in parts if (v := item.strip(' '))]
    except ValueError:
        # Truly invalid, or a valid integer too long for int()
        # (int_max_str_digits); let the exact parser decide.
        return _slow(s)
