import os
from array import array
from functools import reduce
from operator import add


def _part(fs, lo, hi, w):
    return [reduce(add, fs[i:i + w], 0.0) / w for i in range(lo, hi)]


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
    fs = list(map(float, xs))
    k = min(4, os.cpu_count() or 1)
    if k < 2 or n * w < 200000 or not hasattr(os, "fork"):
        return _part(fs, 0, n, w)
    cuts = [n * t // k for t in range(k + 1)]
    kids = []
    try:
        for t in range(1, k):
            rd, wr = os.pipe()
            pid = os.fork()
            if pid == 0:
                try:
                    os.close(rd)
                    data = array('d', _part(fs, cuts[t], cuts[t + 1], w)).tobytes()
                    with os.fdopen(wr, 'wb') as f:
                        f.write(data)
                finally:
                    os._exit(0)
            os.close(wr)
            kids.append((t, pid, rd))
    except OSError:
        pass
    parts = {0: _part(fs, cuts[0], cuts[1], w)}
    for t, pid, rd in kids:
        with os.fdopen(rd, 'rb') as f:
            b = f.read()
        os.waitpid(pid, 0)
        a = array('d')
        a.frombytes(b)
        if len(a) == cuts[t + 1] - cuts[t]:
            parts[t] = a.tolist()
    out = []
    for t in range(k):
        out += parts[t] if t in parts else _part(fs, cuts[t], cuts[t + 1], w)
    return out
