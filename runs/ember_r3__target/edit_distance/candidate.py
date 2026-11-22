def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if a == b:
        return 0
    n = len(a)
    m = len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    # Bit-parallel Myers algorithm works on the shorter string.
    if m > n:
        a, b = b, a
        n, m = m, n
    masks = {}
    for i, ch in enumerate(b):
        masks[ch] = masks.get(ch, 0) | (1 << i)
    ALL = (1 << m) - 1
    pv = ALL
    mv = 0
    score = m
    top = 1 << (m - 1)
    get = masks.get
    for ch in a:
        eq = get(ch, 0)
        xv = eq | mv
        xh = (((eq & pv) + pv) ^ pv) | eq
        xh &= ALL
        ph = mv | (ALL ^ (xh | pv))
        mh = pv & xh
        if ph & top:
            score += 1
        if mh & top:
            score -= 1
        ph = ((ph << 1) | 1) & ALL
        mh = (mh << 1) & ALL
        pv = mh | (ALL ^ (xv | ph))
        mv = ph & xv
    return score
