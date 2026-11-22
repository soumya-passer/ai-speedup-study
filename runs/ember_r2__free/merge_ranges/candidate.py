def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    if not ranges:
        return []
    it = iter(sorted(ranges))
    cur_s, cur_e = next(it)
    out = []
    append = out.append
    for s, e in it:
        if s <= cur_e:
            if e > cur_e:
                cur_e = e
        else:
            append((cur_s, cur_e))
            cur_s, cur_e = s, e
    append((cur_s, cur_e))
    return out
