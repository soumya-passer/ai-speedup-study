def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    # Bit-parallel Myers / Hyyrö algorithm: use the shorter string as the
    # pattern so the big-int bitmasks are as small as possible.
    if len(a) < len(b):
        a, b = b, a
    m = len(b)
    mask = (1 << m) - 1
    peq = {}
    for i, ch in enumerate(b):
        peq[ch] = peq.get(ch, 0) | (1 << i)
    get = peq.get
    pv = mask
    mv = 0
    score = m
    top = 1 << (m - 1)
    for ch in a:
        eq = get(ch, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) ^ pv) | eq) & mask
        ph = mv | (mask ^ (xh | pv))
        mh = pv & xh
        if ph & top:
            score += 1
        if mh & top:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = mh | (mask ^ (xv | ph))
        mv = ph & xv
    return score
