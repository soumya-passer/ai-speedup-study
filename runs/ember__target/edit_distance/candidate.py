def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    # Bit-parallel Levenshtein (Hyyrö / Myers bit-vector algorithm).
    # Python arbitrary-precision ints make the bit operations run in C.
    if a == b:
        return 0
    # Make b the pattern (bit-vector length). Keep it the shorter string
    # so the big ints stay small; the algorithm is symmetric.
    if len(a) < len(b):
        a, b = b, a
    n, m = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m

    # Eq masks: bit j set iff b[j] == character.
    masks = {}
    for i, ch in enumerate(b):
        masks[ch] = masks.get(ch, 0) | (1 << i)

    mask_all = (1 << m) - 1
    Pv = mask_all
    Mv = 0
    score = m
    top = 1 << (m - 1)
    get = masks.get

    for ch in a:
        Eq = get(ch, 0)
        Xv = Eq | Mv
        Xh = ((((Eq & Pv) + Pv) & mask_all) ^ Pv) | Eq
        Ph = Mv | (mask_all ^ (Xh | Pv))
        Mh = Pv & Xh
        if Ph & top:
            score += 1
        if Mh & top:
            score -= 1
        Ph = ((Ph << 1) | 1) & mask_all
        Mh = (Mh << 1) & mask_all
        Pv = Mh | (mask_all ^ (Xv | Ph))
        Mv = Ph & Xv
    return score
