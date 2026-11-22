def moving_average(xs, w):
    if w < 1:
        raise ValueError("w < 1")
    n = len(xs)
    m = n - w + 1
    if m <= 0:
        return []
    s = sum
    # Fast path: reuse sequence directly when elements are float/int/bool.
    # sum(slice, 0.0) adds left-to-right from 0.0 in C -> bit-identical.
    try:
        t = type(xs[0])
        if t is float or t is int or t is bool:
            f = xs
            return [s(f[i:i + w], 0.0) / w for i in range(m)]
    except Exception:
        pass
    f = list(map(float, xs))
    return [s(f[i:i + w], 0.0) / w for i in range(m)]
