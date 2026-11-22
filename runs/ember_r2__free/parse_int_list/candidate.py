from itertools import repeat


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
    # int() in C accepts things the spec rejects: underscores,
    # non-space whitespace (incl. \x1c-\x1f) and unicode digits.
    # Detect those (non-ascii covers unicode) and fall back to the
    # exact slow parser, which raises ValueError for them.
    # isascii() is O(1) for ascii strings; `in` for a single char
    # is a memchr-style C scan.
    if not s.isascii() or "_" in s or "\t" in s or "\n" in s or "\r" in s or "\f" in s or "\v" in s or "\x1c" in s or "\x1d" in s or "\x1e" in s or "\x1f" in s:
        return _slow(s)
    parts = s.split(",")
    try:
        # Fast path: int() itself strips the surrounding spaces.
        # Handles the common benchmark case (no empty items).
        return list(map(int, parts))
    except ValueError:
        pass
    try:
        # Empty / space-only items: strip only ' ' (not other
        # whitespace, already excluded) and drop empties, in C via
        # map/filter. int() still rejects interior spaces/signs.
        return list(map(int, filter(None, map(str.strip, parts, repeat(" ")))))
    except ValueError:
        # Invalid item, or int() digit-limit for a huge number:
        # the slow parser either raises ValueError("bad item")
        # or returns the (huge) correct result.
        return _slow(s)
