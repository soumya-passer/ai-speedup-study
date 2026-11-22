def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    m = len(a)
    if m == 0:
        return len(b)
    peq = {}
    bit = 1
    for c in a:
        peq[c] = peq.get(c, 0) | bit
        bit <<= 1
    mask = bit - 1
    top = bit >> 1
    pv = mask
    mv = 0
    score = m
    for c in b:
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) ^ pv) | eq) & mask
        ph = (mv | ~(xh | pv)) & mask
        mh = pv & xh
        if ph & top:
            score += 1
        elif mh & top:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = (mh | ~(xv | ph)) & mask
        mv = ph & xv
    return score
