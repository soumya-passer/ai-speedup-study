def parse_int_list(s):
    out = []
    append = out.append
    for item in s.split(","):
        t = item.strip(" ")
        if not t:
            continue
        f = ord(t[0])
        if f == 43 or f == 45:
            pass
        elif 48 <= f <= 57:
            pass
        else:
            raise ValueError("bad item")
        if not 48 <= ord(t[-1]) <= 57:
            raise ValueError("bad item")
        if "_" in t or not t.isascii():
            raise ValueError("bad item")
        append(int(t))
    return out
