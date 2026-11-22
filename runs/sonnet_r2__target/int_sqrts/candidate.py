from math import isqrt


def int_sqrts(ns):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    try:
        return [isqrt(n) for n in ns]
    except ValueError:
        raise ValueError("negative") from None
