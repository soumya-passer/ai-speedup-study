from math import sqrt
from operator import mul, sub
from itertools import repeat


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = sum(xs) / n
    var = sum(map(mul, xs, xs)) / n - mean * mean
    if var < 0 or mean * mean > var * 1000000:
        shift = xs[0]
        devs = list(map(sub, xs, repeat(shift)))
        mean_dev = sum(devs) / n
        var = sum(map(mul, devs, devs)) / n - mean_dev * mean_dev
        mean = shift + mean_dev
        if var < 0:
            var = 0
    return (float(mean), sqrt(var))
