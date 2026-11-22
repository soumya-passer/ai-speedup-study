def normalize(xs):
    """Scale numbers to the range 0 to 1: (x - min) / (max - min).
    If all values are equal, every result is 0.0. An empty list gives [].
    Returns a new list; the input list must not change."""
    if not xs:
        return []
    lo = min(xs)
    hi = max(xs)
    rng = hi - lo
    if rng == 0:
        return [0.0] * len(xs)
    return [(x - lo) / rng for x in xs]
