def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    This version works in exact fractions, so it is as accurate as possible.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    from fractions import Fraction
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    exact = [Fraction(x) for x in xs]
    mean = sum(exact) / n
    var = sum((x - mean) ** 2 for x in exact) / n
    return (float(mean), float(var) ** 0.5)
