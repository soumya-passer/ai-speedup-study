from math import isqrt

def int_sqrts(ns):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    out = []
    append = out.append
    _isqrt = isqrt
    for n in ns:
        if n < 0:
            raise ValueError("negative")
        append(_isqrt(n))
    return out
