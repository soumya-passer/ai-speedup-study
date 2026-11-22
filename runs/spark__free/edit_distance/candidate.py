def edit_distance(a, b):
    """Myers' bit-parallel Levenshtein (O((m/w)*n) using Python ints)."""
    if a == b:
        return 0
    la = len(a)
    lb = len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    # make a the shorter (pattern) -> fewer bits
    if la > lb:
        a, b = b, a
        la, lb = lb, la
    m = la
    if m == 1:
        return lb - 1 if a[0] in b else lb
    # Peq: char -> bitmask of positions in pattern
    peq = {}
    bit = 1
    for ch in a:
        peq[ch] = peq.get(ch, 0) | bit
        bit <<= 1
    mask = bit - 1  # (1 << m) - 1, all m bits set
    top = bit >> 1  # 1 << (m-1)
    VP = mask
    VN = 0
    score = m
    get = peq.get
    for ch in b:
        Eq = get(ch, 0)
        Xv = Eq | VN
        Xh = (((Eq & VP) + VP) ^ VP) | Eq
        Ph = (VN | ~(Xh | VP)) & mask
        Mh = VP & Xh
        if Ph & top:
            score += 1
        elif Mh & top:
            score -= 1
        Ph = (Ph << 1) | 1
        Mh <<= 1
        VP = (Mh | ~(Xv | Ph)) & mask
        VN = Ph & Xv
    return score
