def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n, m = len(a), len(b)
    # strip common prefix and suffix
    s = 0
    while s < n and s < m and a[s] == b[s]:
        s += 1
    while n > s and m > s and a[n - 1] == b[m - 1]:
        n -= 1
        m -= 1
    a = a[s:n]
    b = b[s:m]
    n -= s
    m -= s
    if n == 0:
        return m
    if m == 0:
        return n
    if m > n:
        a, b = b, a
        n, m = m, n
    # b is the shorter; row has length m+1
    prev = list(range(m + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        left = i
        for cb, diag, up in zip(b, prev, prev[1:]):
            x = diag if ca == cb else diag + 1
            up += 1
            left += 1
            if up < x:
                x = up
            if left < x:
                x = left
            cur.append(x)
            left = x
        prev = cur
    return prev[m]
