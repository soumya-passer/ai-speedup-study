def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        append = cur.append
        left = i
        for cb, diag, up in zip(b, prev, prev[1:]):
            v = diag + (ca != cb)
            u = up + 1
            if u < v:
                v = u
            l = left + 1
            if l < v:
                v = l
            append(v)
            left = v
        prev = cur
    return prev[-1]
