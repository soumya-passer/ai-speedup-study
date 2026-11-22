def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if len(a) < len(b):
        a, b = b, a
    m = len(b)
    if m == 0:
        return len(a)
    # Myers bit-parallel Levenshtein: b is the pattern, a is the text.
    peq = {}
    bit = 1
    for c in b:
        peq[c] = peq.get(c, 0) | bit
        bit <<= 1
    mask = (1 << m) - 1
    high = 1 << (m - 1)
    pv = mask
    mv = 0
    score = m
    get = peq.get
    for c in a:
        eq = get(c, 0)
        xv = eq | mv
        xh = (((eq & pv) + pv) ^ pv) | eq
        ph = mv | ~(xh | pv)
        mh = pv & xh
        if ph & high:
            score += 1
        elif mh & high:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = (mh | ~(xv | ph)) & mask
        mv = ph & xv
    return score
