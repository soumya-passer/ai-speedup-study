from math import fsum


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = fsum(xs) / n
    var = fsum([(x - mean) ** 2 for x in xs]) / n
    return (mean, var ** 0.5)
