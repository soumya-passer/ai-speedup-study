def int_sqrts(ns):
    """For each non-negative int n (it can be very large, up to 10**40),
    the largest int r with r*r <= n. Raises ValueError on a negative n."""
    out = []
    for n in ns:
        if n < 0:
            raise ValueError("negative")
        lo, hi = 0, n + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid * mid <= n:
                lo = mid
            else:
                hi = mid
        out.append(lo)
    return out
