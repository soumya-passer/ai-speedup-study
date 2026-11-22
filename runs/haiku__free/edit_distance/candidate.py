def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    # Edit distance is symmetric, so make b the shorter string to keep rows short.
    if len(a) < len(b):
        a, b = b, a
    m = len(b)
    prev = list(range(m + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        left = i
        for j in range(1, m + 1):
            x = prev[j] + 1
            y = left + 1
            if y < x:
                x = y
            z = prev[j - 1] if ca == b[j - 1] else prev[j - 1] + 1
            if z < x:
                x = z
            cur.append(x)
            left = x
        prev = cur
    return prev[m]
