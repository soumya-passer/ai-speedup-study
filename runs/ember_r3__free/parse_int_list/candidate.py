from json import loads as _json_loads


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


def _map_fallback(s):
    try:
        return list(map(int, s.split(",")))
    except ValueError:
        pass
    try:
        return list(map(int, filter(None, map(str.strip, s.split(",")))))
    except ValueError:
        return _slow(s)


def parse_int_list(s):
    if type(s) is not str:
        return _slow(s)
    try:
        b = s.encode("ascii")
    except UnicodeEncodeError:
        return _slow(s)
    # Spec alphabet only: digits, comma, space, + -. Any other
    # character (letters, '.', '_', tab, '"', unicode, ...) makes
    # the original raise ValueError, so route to _slow (which will).
    # This also guards JSON: with this alphabet a successful JSON
    # parse can only be a list of ints (no floats/strings/bools).
    if b.translate(None, b"0123456789, +-"):
        return _slow(s)
    try:
        return _json_loads("[" + s + "]")
    except Exception:
        # JSON rejects '+', leading zeros, empty items, huge ints,
        # '1-2', etc. All of those are handled exactly by int()/slow.
        return _map_fallback(s)
