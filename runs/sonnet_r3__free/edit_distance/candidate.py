def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n, m = len(a), len(b)
    if n < m:
        a, b, n, m = b, a, m, n
    # b is the shorter sequence; one rolling row of length m + 1.
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        ai = a[i - 1]
        left = i
        diag = prev[0]
        cur = [i]
        app = cur.append
        j = 0
        for bj in b:
            j += 1
            up = prev[j]
            if ai == bj:
                v = diag
            else:
                v = diag if diag < up else up
                if left < v:
                    v = left
                v += 1
            app(v)
            left = v
            diag = up
        prev = cur
    return prev[m]
