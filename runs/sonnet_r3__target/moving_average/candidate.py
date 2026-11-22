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
    # 0.0 + x is what the first add of every window does (turns -0.0 into 0.0),
    # so each window can start from its first element with no start value.
    fs = [0.0 + float(x) * 1.0 for x in xs]
    if w == 1:
        return [t / 1 for t in fs]
    # A complex number adds its real and imaginary parts as two separate float
    # adds, so one reduce computes two neighbouring windows in the same order.
    c = list(map(complex, fs, fs[1:] + [0.0]))
    r = reduce
    a = add
    out = []
    app = out.append
    for i in range(0, n, 2):
        z = r(a, c[i:i + w])
        app(z.real / w)
        app(z.imag / w)
    if len(out) > n:
        out.pop()
    return out
