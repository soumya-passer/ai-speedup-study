def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    out = []
    for i in range(len(xs) - w + 1):
        total = 0.0
        for j in range(i, i + w):
            total = total + float(xs[j]) * 1.0
        out.append(total / w)
    return out
