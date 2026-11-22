def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b.

    Bit-parallel Levenshtein distance (Hyyrö).  The DP row for b is
    packed into two Python integers, Pv/Mv, whose bits hold the
    +1/-1 differences between neighbouring cells in the row.  The
    next row is then a handful of big-integer operations (in C) per
    character of a instead of m Python-level min/add operations.
    """
    if a == b:
        return 0
    n = len(a)
    m = len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    # Symmetric; keep b the shorter string so bit-vectors are narrow.
    if m > n:
        a, b = b, a
        n, m = m, n

    # S[c]: bit j set iff b[j] == c.
    masks = {}
    bit = 1
    for ch in b:
        masks[ch] = masks.get(ch, 0) | bit
        bit <<= 1

    # Precompute the Eq bit-vector for every character of a.
    get = masks.get
    eqs = [get(ch, 0) for ch in a]

    all_ones = (1 << m) - 1
    top = 1 << (m - 1)

    Pv = all_ones   # all +1 differences
    Mv = 0          # no -1 differences
    score = m       # distance for the empty prefix of a

    for Eq in eqs:
        Xv = Eq | Mv
        Xh = (((Eq & Pv) + Pv) ^ Pv) | Eq
        Ph = Mv | ~(Xh | Pv)
        Mh = Pv & Xh
        if Ph & top:
            score += 1
        if Mh & top:
            score -= 1
        # Shift horizontal vectors right by one column; the 1 injected
        # into Ph is the forced +1 difference in column 0.
        # Ph/Mh high bits beyond m are discarded implicitly: Pv is
        # masked below and Mv = Ph & Xv stays < 2**m since Xv < 2**m.
        Ph = (Ph << 1) | 1
        Mh <<= 1
        Pv = (Mh | ~(Xv | Ph)) & all_ones
        Mv = Ph & Xv

    return score
