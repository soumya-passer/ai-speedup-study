def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    rs = sorted(map(tuple, ranges))
    if not rs:
        return []
    merged = []
    append = merged.append
    cur_s, cur_e = rs[0]
    for s, e in rs[1:]:
        if s <= cur_e:
            if e > cur_e:
                cur_e = e
        else:
            append((cur_s, cur_e))
            cur_s = s
            cur_e = e
    append((cur_s, cur_e))
    return merged
