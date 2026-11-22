def _simple(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        left = i
        for j, cb in enumerate(b):
            v = prev[j] + (ca != cb)
            u = prev[j + 1] + 1
            if u < v:
                v = u
            left += 1
            if left < v:
                v = left
            else:
                left = v
            cur.append(left)
        prev = cur
    return prev[-1]


def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    if m > n:
        a, b, n, m = b, a, m, n
    # Bit-parallel (Myers/Hyyro): bit i of the masks tracks position i of b.
    try:
        peq = {}
        for i, c in enumerate(b):
            peq[c] = peq.get(c, 0) | (1 << i)
    except TypeError:
        return _simple(a, b)
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
