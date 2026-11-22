def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    n = len(ranges)
    if n == 0:
        return []
    if n == 1:
        r = ranges[0]
        return [(r[0], r[1])]
    rs = sorted(ranges)
    out = []
    cur_s = rs[0][0]
    cur_e = rs[0][1]
    for r in rs[1:]:
        s = r[0]
        e = r[1]
        if s <= cur_e:
            if e > cur_e:
                cur_e = e
        else:
            out.append((cur_s, cur_e))
            cur_s = s
            cur_e = e
    out.append((cur_s, cur_e))
    return out
