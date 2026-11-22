def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    rs = sorted(ranges)
    if not rs:
        return []
    merged = []
    append = merged.append
    it = iter(rs)
    cur_start, cur_end = next(it)
    for s, e in it:
        if s <= cur_end:
            if e > cur_end:
                cur_end = e
        else:
            append((cur_start, cur_end))
            cur_start, cur_end = s, e
    append((cur_start, cur_end))
    return merged
