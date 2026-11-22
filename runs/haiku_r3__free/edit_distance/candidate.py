def edit_distance(a, b):
    """Fewest single-character inserts, deletes or swaps to turn a into b."""
    if len(a) > len(b):
        a, b = b, a  # distance is symmetric; the shorter string is the bit pattern
    m = len(a)
    if m == 0:
        return len(b)
    try:
        # Bit-parallel Myers/Hyyro: bit i of peq[c] is set when a[i] == c.
        peq = {}
        for i, ch in enumerate(a):
            peq[ch] = peq.get(ch, 0) | (1 << i)
    except TypeError:  # unhashable items: plain dynamic programming
        return _dp(a, b)
    full = (1 << m) - 1
    high = 1 << (m - 1)
    pv, mv, score = full, 0, m
    for ch in b:
        eq = peq.get(ch, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) ^ pv) | eq)
        ph = mv | (~(xh | pv) & full)
        mh = pv & xh
        if ph & high:
            score += 1
        elif mh & high:
            score -= 1
        ph = ((ph << 1) | 1) & full
        mh = (mh << 1) & full
        pv = mh | (~(xv | ph) & full)
        mv = ph & xv
    return score


def _dp(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
    return d[n][m]
