def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    rs = sorted(ranges)
    if not rs:
        return []
    it = iter(rs)
    group = next(it)
    cs, ce = group
    dirty = type(group) is not tuple
    merged = []
    append = merged.append
    for t in it:
        s, e = t
        if s <= ce:
            if e > ce:
                ce = e
                dirty = True
        else:
            append((cs, ce) if dirty else group)
            group = t
            cs, ce = s, e
            dirty = type(group) is not tuple
    append((cs, ce) if dirty else group)
    return merged
