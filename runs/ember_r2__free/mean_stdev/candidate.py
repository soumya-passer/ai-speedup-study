from math import sqrt, fsum
from operator import mul, sub
from itertools import repeat


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Floats may differ from exact result only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")

    # Exact integer path (shifted by first element): integer arithmetic
    # is exact and avoids Fraction gcd overhead.
    if type(xs[0]) is int:
        c = xs[0]
        ds = list(map(sub, xs, repeat(c)))
        s_d = sum(ds)
        if type(s_d) is int:
            ss_d = sum(map(mul, ds, ds))
            mean = (c * n + s_d) / n
            var = (ss_d * n - s_d * s_d) / (n * n)
            return (float(mean), sqrt(var))
        # Mixed int/float input: fall through to the float path.

    # Fast path: one C-level sum for the mean and one C-level
    # map(mul) sum for the second moment.  sum(map(...)) runs in C
    # (operator.mul is a C function), avoiding a Python generator.
    s = sum(xs)
    ss = sum(map(mul, xs, xs))
    mean = s / n
    ex2 = ss / n
    var = ex2 - mean * mean

    # Ill-conditioned case: var << ex2 means catastrophic cancellation
    # in ex2 - mean**2 (e.g. large offset, small variance).  Fall back
    # to the stable two-pass algorithm about an accurately computed
    # mean (fsum), which is still C-level via map/sub/mul.
    if var < ex2 * 1e-2:
        mean = fsum(xs) / n
        var = fsum(map(mul, map(sub, xs, repeat(mean)),
                       map(sub, xs, repeat(mean)))) / n

    return (float(mean), sqrt(var) if var > 0.0 else 0.0)
