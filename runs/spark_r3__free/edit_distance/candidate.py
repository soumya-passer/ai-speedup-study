def edit_distance(a, b):
    la = len(a)
    lb = len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    if a == b:
        return 0
    if la > lb:
        a, b = b, a
        la, lb = lb, la
    m = la
    Peq = {}
    bit = 1
    get_d = Peq.get
    for ch in a:
        Peq[ch] = get_d(ch, 0) | bit
        bit <<= 1
    mask = bit - 1
    top = bit >> 1
    pv = mask
    mv = 0
    score = m
    get = Peq.get
    _mask = mask
    _top = top
    for ch in b:
        eq = get(ch, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) & _mask) ^ pv) | eq
        ph = mv | (~(xh | pv) & _mask)
        mh = pv & xh
        if ph & _top:
            score += 1
        elif mh & _top:
            score -= 1
        ph = ((ph << 1) | 1) & _mask
        mh = (mh << 1) & _mask
        pv = mh | (~(xv | ph) & _mask)
        mv = ph & xv
    return score
