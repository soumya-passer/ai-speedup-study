def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    # masks for b (bit j = 1 if b[j] == c), LSB = b[0]
    masks = {}
    for j, ch in enumerate(b):
        masks[ch] = masks.get(ch, 0) | (1 << j)
    all_bits = (1 << m) - 1
    Pv = all_bits
    Mv = 0
    score = m
    top = 1 << (m - 1)
    get = masks.get
    for ch in a:
        Eq = get(ch, 0)
        Xv = Eq | Mv
        Xh = (((Eq & Pv) + Pv) ^ Pv) | Eq
        Ph = Mv | ~(Xh | Pv)
        Mh = Pv & Xh
        if Ph & top:
            score += 1
        if Mh & top:
            score -= 1
        Ph = ((Ph << 1) | 1) & all_bits
        Pv = (Mh | ~(Xh | Ph)) & all_bits
        Mv = (Ph & Xh) & all_bits
    return score
