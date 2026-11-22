def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    fs = list(map(float, xs))
    out = []
    ap = out.append
    for i in range(len(fs) - w + 1):
        t = 0.0
        for x in fs[i:i + w]:
            t += x
        ap(t / w)
    return out
