from itertools import islice, repeat
from operator import add, truediv


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
    ys = [float(x) * 1.0 for x in xs]
    # acc[i] holds the running total of window i. Each pass adds the next
    # element of every window, so each window still sums left to right.
    acc = [0.0] * n
    for j in range(w):
        acc = list(map(add, acc, islice(ys, j, None)))
    return list(map(truediv, acc, repeat(w, n)))
