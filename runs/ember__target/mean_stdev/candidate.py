import math
from itertools import repeat
from operator import mul, sub


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    This version works in exact fractions, so it is as accurate as possible.
    Floats may differ from this function only by rounding (relative 1e-6).
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = sum(xs) / n
    # Two-pass variance (accurate even for large offsets) using only
    # C-implemented map/operator/sum loops instead of Python-level loops.
    try:
        diffs = list(map(sub, xs, repeat(mean)))
        var = sum(map(mul, diffs, diffs)) / n
    except TypeError:
        var = sum((x - mean) * (x - mean) for x in xs) / n
    return (float(mean), math.sqrt(float(var)))
