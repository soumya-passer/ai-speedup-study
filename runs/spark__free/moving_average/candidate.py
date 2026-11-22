def moving_average(xs, w):
    if w < 1:
        raise ValueError("w < 1")
    n = len(xs)
    m = n - w + 1
    if m <= 0:
        return []
    if w == 1:
        # bit-identical to (0.0 + float(x)*1.0)/1; 0.0 seed matters for -0.0
        return [(0.0 + float(x)) / w for x in xs]
    fxs = list(map(float, xs))
    s = sum
    ww = w
    return [s(fxs[i:i + ww]) / ww for i in range(m)]
