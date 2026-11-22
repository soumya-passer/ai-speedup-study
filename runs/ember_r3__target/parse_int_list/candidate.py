def _parse_slow(s):
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
    # Fast path uses C int(). int() differs from the spec for some
    # inputs: it accepts underscores, non-space whitespace, and
    # non-ASCII (unicode) digits/whitespace. If any of those are
    # present, fall back to the exact original parser.
    if (
        not s.isascii()
        or "_" in s
        or "\t" in s
        or "\n" in s
        or "\r" in s
        or "\v" in s
        or "\f" in s
        or "\x1c" in s
        or "\x1d" in s
        or "\x1e" in s
        or "\x1f" in s
    ):
        return _parse_slow(s)

    parts = s.split(",")
    try:
        # map(int, ...) runs the conversion loop in C.
        return list(map(int, parts))
    except ValueError:
        pass

    # int() failed: could be empty items (to skip), a genuinely bad
    # item (to raise), or a number with >4300 digits (int limit).
    # Handle empties with int() and defer everything else to slow.
    try:
        return [int(p) for p in parts if p.strip(" ")]
    except ValueError:
        return _parse_slow(s)
