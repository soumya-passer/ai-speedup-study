def merge_ranges(ranges):
    if not ranges:
        return []
    sr = sorted(ranges)
    cs, ce = sr[0]
    out = []
    append = out.append
    for s, e in sr[1:]:
        if s <= ce:
            if e > ce:
                ce = e
        else:
            append((cs, ce))
            cs = s
            ce = e
    append((cs, ce))
    return out
