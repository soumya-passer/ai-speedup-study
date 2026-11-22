import math

def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    m = math.fsum(xs) / n
    # two-pass: numerically stable for typical data, still C-accelerated
    v = math.fsum((x - m) * (x - m) for x in xs) / n
    if v < 0.0:
        v = 0.0
    return (m, math.sqrt(v))
