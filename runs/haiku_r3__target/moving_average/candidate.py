from functools import reduce
from operator import add


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    n = len(xs) - w + 1
    if n <= 0:
        return []
    # Convert each value once. float(x) * 1.0 equals float(x), so this matches the original.
    vals = tuple(float(x) * 1.0 for x in xs)
    # reduce adds each window left to right from 0.0 in C, the same order as the original loop.
    return [reduce(add, vals[i:i + w], 0.0) / w for i in range(n)]
