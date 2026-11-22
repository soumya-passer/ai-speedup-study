def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n = len(a)
    if n == 0:
        return len(b)
    # Bit-parallel (Myers / Hyyro) algorithm: bit i of each mask is row i+1
    # of the DP table for the current column of b.
    peq = {}
    for i, c in enumerate(a):
        peq[c] = peq.get(c, 0) | (1 << i)
    mask = (1 << n) - 1
    high = 1 << (n - 1)
    pv = mask
    mv = 0
    score = n
    for c in b:
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) & mask) ^ pv) | eq
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
