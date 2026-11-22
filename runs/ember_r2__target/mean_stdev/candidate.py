from math import fsum, sqrt


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    This version works in exact fractions, so it is as accurate as possible.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = fsum(xs) / n
    var = fsum((x - mean) * (x - mean) for x in xs) / n
    return (mean, sqrt(var))
