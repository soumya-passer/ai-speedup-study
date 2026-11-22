from math import fsum, sqrt


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    m = fsum(xs) / n
    var = fsum([(x - m) * (x - m) for x in xs]) / n
    return (m, sqrt(var))
