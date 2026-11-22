def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    rs = [tuple(r) for r in ranges]
    changed = True
    while changed:
        changed = False
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, b = rs[i], rs[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    rs[i] = (min(a[0], b[0]), max(a[1], b[1]))
                    del rs[j]
                    changed = True
                    break
            if changed:
                break
    return sorted(rs)
