import math as _math

def int_sqrts(ns, _isqrt=_math.isqrt):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    try:
        return list(map(_isqrt, ns))
    except ValueError:
        for n in ns:
            if n < 0:
                raise ValueError("negative") from None
        raise
