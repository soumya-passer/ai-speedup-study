def merge_ranges(ranges):
    if not ranges:
        return []
    sr = sorted(ranges)
    out = []
    append = out.append
    it = iter(sr)
    f = next(it)
    cs, ce = f[0], f[1]
    for r in it:
        s, e = r
        if s <= ce:
            if e > ce:
                ce = e
        else:
            append((cs, ce))
            cs, ce = s, e
    append((cs, ce))
    return out
