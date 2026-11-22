from math import isqrt as _isqrt


def int_sqrts(ns):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    return list(map(_isqrt, ns))
