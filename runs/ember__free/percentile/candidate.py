def percentile(xs, p):
    """The p-th percentile (0 <= p <= 100) of a list of numbers, by linear
    blending: sort the list, find position r = p / 100 * (n - 1), and blend
    the items at floor(r) and floor(r) + 1 by the fraction part of r.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list or p outside 0 to 100."""
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
