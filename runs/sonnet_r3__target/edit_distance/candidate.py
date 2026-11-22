def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n = len(a)
    if n == 0:
        return len(b)
    if not b:
        return n
    # Bit-parallel Levenshtein (Myers / Hyyro), one big integer per row.
    peq = {}
    bit = 1
    for ch in a:
        peq[ch] = peq.get(ch, 0) | bit
        bit <<= 1
    mask = (1 << n) - 1
    hb = 1 << (n - 1)
    pv = mask
    mv = 0
    score = n
    get = peq.get
    for ch in b:
        eq = get(ch, 0)
        xv = eq | mv
        xh = (((eq & pv) + pv) ^ pv) | eq
        ph = (mv | ~(xh | pv)) & mask
        mh = pv & xh
        if ph & hb:
            score += 1
        elif mh & hb:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = (mh | ~(xv | ph)) & mask
        mv = ph & xv
    return score
