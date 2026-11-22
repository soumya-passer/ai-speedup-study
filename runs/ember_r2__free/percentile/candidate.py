def percentile(xs, p):
    if not xs or p < 0 or p > 100:
        raise ValueError("bad input")
    s = sorted(xs)
    n = len(s)
    r = p / 100 * (n - 1)
    lo = int(r)
    frac = r - lo
    if lo + 1 < n:
        return s[lo] + (s[lo + 1] - s[lo]) * frac
    return float(s[lo])
