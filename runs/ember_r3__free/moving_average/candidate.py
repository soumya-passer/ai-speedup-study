class _Float(float):
    __slots__ = ()


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    n = len(xs)
    if w > n:
        return []
    # sum() uses compensated (Neumaier) summation on plain-float lists,
    # which differs from a plain left-to-right fold. On a list of float
    # *subclass* instances it falls back to the generic C addition loop:
    # still exact left-to-right float addition, but driven from C instead
    # of a Python-level loop. Convert once, then slice+sum per window.
    data = list(map(_Float, xs))
    add_all = sum
    return [add_all(data[i:i + w]) / w for i in range(n - w + 1)]
