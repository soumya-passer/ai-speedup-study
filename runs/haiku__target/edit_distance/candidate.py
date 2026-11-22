def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    m = len(a)
    if m == 0:
        return len(b)
    # Bit-parallel (Myers / Hyyro) variant: one big-int row per character of b.
    peq = {}
    for i, c in enumerate(a):
        peq[c] = peq.get(c, 0) | (1 << i)
    mask = (1 << m) - 1
    high = 1 << (m - 1)
    pv = mask
    mv = 0
    score = m
    for c in b:
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) ^ pv) | eq)
        ph = mv | (~(xh | pv) & mask)
        mh = pv & xh
        if ph & high:
            score += 1
        elif mh & high:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = mh | (~(xv | ph) & mask)
        mv = ph & xv
    return score
