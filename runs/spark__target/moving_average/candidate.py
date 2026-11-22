def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    n = len(xs)
    m = n - w + 1
    if m <= 0:
        return []
    # Convert once: float(x)*1.0 == float(x) bit-for-bit (mult by 1.0 is exact),
    # so vals[j] equals the per-element term of the reference loop.
    vals = list(map(float, xs))
    out = [0.0] * m
    _sum = sum
    # sum(vals[i:i+w]) adds left-to-right starting from int 0;
    # 0 + x == 0.0 + x bit-for-bit, rest of order identical to reference.
    # Runs in C, much faster than Python inner loop.
    for i in range(m):
        out[i] = _sum(vals[i:i + w]) / w
    return out
