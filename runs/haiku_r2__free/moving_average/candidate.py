from functools import reduce
from operator import add


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    count = len(xs) - w + 1
    if count <= 0:
        return []
    # Convert each element once. Every element lies in at least one window,
    # so this does the same float() work as the original, just not repeatedly.
    ys = [float(x) * 1.0 for x in xs]
    # reduce(add, ...) sums left to right from 0.0, like the original loop.
    # Do not use sum(): newer Python versions sum floats differently.
    return [reduce(add, ys[i:i + w], 0.0) / w for i in range(count)]
