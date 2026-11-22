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
    vals = [float(x) * 1.0 for x in xs]
    # Each window is summed left to right from 0.0 by a C-level reduce,
    # which keeps the rounding identical to the original loop.
    return [reduce(add, vals[i:i + w], 0.0) / w for i in range(n)]
