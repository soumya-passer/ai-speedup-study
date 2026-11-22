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
    # Convert once; every element lands in some window, so the original
    # would also have converted all of them.
    fs = [float(x) for x in xs]
    # reduce(add) sums each window left to right from 0.0 in C, which keeps
    # the same rounding as the original loop (unlike sum(), which may differ).
    return [reduce(add, fs[i:i + w], 0.0) / w for i in range(n)]
