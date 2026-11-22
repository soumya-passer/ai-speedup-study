def normalize(xs):
    """Scale numbers to the range 0 to 1: (x - min) / (max - min).
    If all values are equal, every result is 0.0. An empty list gives [].
    Returns a new list; the input list must not change."""
    out = []
    for x in xs:
        lo = min(xs)
        hi = max(xs)
        if hi == lo:
            out.append(0.0)
        else:
            out.append((x - lo) / (hi - lo))
    return out
