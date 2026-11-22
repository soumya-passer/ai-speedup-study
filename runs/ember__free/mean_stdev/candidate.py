from math import sqrt
from operator import mul, sub
from itertools import repeat


def mean_stdev(xs):
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    mean = sum(xs) / n
    msq = sum(map(mul, xs, xs)) / n
    var = msq - mean * mean
    if var <= msq * 1e-4:
        diffs = list(map(sub, xs, repeat(mean)))
        var = sum(map(mul, diffs, diffs)) / n
    return (mean, sqrt(var))
