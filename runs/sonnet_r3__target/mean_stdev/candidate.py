def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Uses math.fsum (exactly rounded sums) instead of Fractions.
    Raises ValueError on an empty list."""
    from math import fsum, sqrt
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = fsum(xs) / n
    var = fsum([(x - mean) * (x - mean) for x in xs]) / n
    return (mean, sqrt(var))
