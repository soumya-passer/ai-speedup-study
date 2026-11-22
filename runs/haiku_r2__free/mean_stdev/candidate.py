def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    This version uses math.fsum (correctly rounded float sums) instead of Fractions, so it is fast and still accurate.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    from math import fsum
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = fsum(xs) / n
    var = fsum([(x - mean) ** 2 for x in xs]) / n
    return (mean, var ** 0.5)
