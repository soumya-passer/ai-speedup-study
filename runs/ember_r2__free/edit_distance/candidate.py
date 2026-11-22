def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if a == b:
        return 0
    n = len(a)
    m = len(b)
    # Strip common prefix / suffix (preserves Levenshtein distance).
    i = 0
    lim = n if n < m else m
    while i < lim and a[i] == b[i]:
        i += 1
    j = 0
    lim2 = (n - i) if (n - i) < (m - i) else (m - i)
    while j < lim2 and a[n - 1 - j] == b[m - 1 - j]:
        j += 1
    if i or j:
        a = a[i:n - j]
        b = b[i:m - j]
        n = len(a)
        m = len(b)
        if n == 0 or m == 0:
            return n + m
    # Bit-parallel Myers / Hyyrö algorithm.
    # Make b the shorter string (pattern), so big ints are as small as possible.
    if m > n:
        a, b = b, a
        n, m = m, n
    if m == 0:
        return n
    mask = (1 << m) - 1
    top = 1 << (m - 1)
    # S[c] : bitmask of positions of c in b
    S = {}
    bit = 1
    for ch in b:
        S[ch] = S.get(ch, 0) | bit
        bit <<= 1
    get = S.get
    # Pv / Mv encode vertical differences (+1 / -1) of the previous DP row.
    # Initially the row for the empty prefix is 0,1,2,...,m, so all diffs are +1.
    Pv = mask
    Mv = 0
    score = m
    for ch in a:
        Eq = get(ch, 0)
        Xv = Eq | Mv
        Xh = (((Eq & Pv) + Pv) ^ Pv) | Eq
        Ph = Mv | ~(Xh | Pv)
        Mh = Pv & Xh
        if Mh & top:
            score -= 1
        elif Ph & top:
            score += 1
        Ph = (Ph << 1) | 1
        Pv = ((Mh << 1) | ~(Xv | Ph)) & mask
        Mv = Ph & Xv
    return score
