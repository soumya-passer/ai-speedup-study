def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if a == b:
        return 0
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    # Make b the shorter (pattern) so bit-vectors are small.
    if m > n:
        a, b = b, a
        n, m = m, n
    # Peq[c] = bitmask of positions of c in pattern b
    Peq = {}
    for i, ch in enumerate(b):
        Peq[ch] = Peq.get(ch, 0) | (1 << i)
    mask = (1 << m) - 1
    Pv = mask
    Mv = 0
    score = m
    top_bit = 1 << (m - 1)
    get = Peq.get
    for ch in a:
        Eq = get(ch, 0)
        Xv = Eq | Mv
        Xh = ((((Eq & Pv) + Pv) ^ Pv) | Eq) & mask
        Ph = (Mv | ~(Xh | Pv)) & mask
        Mh = Pv & Xh
        if Ph & top_bit:
            score += 1
        elif Mh & top_bit:
            score -= 1
        Ph = ((Ph << 1) | 1) & mask
        Mh = (Mh << 1) & mask
        Pv = (Mh | ~(Xv | Ph)) & mask
        Mv = Ph & Xv
    return score
