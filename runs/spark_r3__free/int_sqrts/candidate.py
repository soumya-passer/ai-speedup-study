import math as _math

def int_sqrts(ns):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    return list(map(_math.isqrt, ns))
