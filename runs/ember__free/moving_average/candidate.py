import operator


class _F(float):
    """Float subclass: CPython's fast sum() path only triggers for exact
    floats, so summing these falls back to a naive C left-to-right loop
    (verified at import below)."""
    __slots__ = ()


def _plain_sum_is_naive():
    try:
        return sum([1e16, 1.0, -1e16], 0.0) == 0.0
    except Exception:
        return False


def _subclass_sum_is_naive():
    try:
        return sum([_F(1e16), _F(1.0), _F(-1e16)], 0.0) == 0.0
    except Exception:
        return False


_PLAIN_NAIVE = _plain_sum_is_naive()
_SUBCLASS_NAIVE = _subclass_sum_is_naive()


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    try:
        w = operator.index(w)
    except TypeError:
        # Original range(len(xs) - w + 1) would raise TypeError here.
        range(len(xs) - w + 1)
        raise
    m = len(xs) - w + 1
    if m <= 0:
        return []
    if _PLAIN_NAIVE:
        ys = list(map(float, xs))
        _sum = sum
        return [_sum(ys[i:i + w], 0.0) / w for i in range(m)]
    if _SUBCLASS_NAIVE:
        fs = list(map(_F, xs))
        _sum = sum
        return [_sum(fs[i:i + w], 0.0) / w for i in range(m)]
    # Fallback (no naive C sum available): vectorise across windows; each
    # step adds the next element of every window, preserving per-window
    # left-to-right order and IEEE rounding at every step.
    from itertools import islice

    ys = list(map(float, xs))
    cum = [0.0 + v for v in ys[:m]]
    for k in range(1, w):
        cum = [a + b for a, b in zip(cum, islice(ys, k, None))]
    return [c / w for c in cum]
