from functools import reduce
from operator import add


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    fx = [float(x) for x in xs]
    # reduce with operator.add keeps strict left-to-right addition from 0.0
    # (unlike sum(), which may use compensated summation).
    return [reduce(add, fx[i:i + w], 0.0) / w for i in range(len(fx) - w + 1)]
