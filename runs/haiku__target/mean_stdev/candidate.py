import math


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Uses float arithmetic with math.fsum (correctly rounded sums), two passes.
    Floats may differ from the exact-fraction version only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = math.fsum(xs) / n
    var = math.fsum([(x - mean) ** 2 for x in xs]) / n
    return (mean, var ** 0.5)
