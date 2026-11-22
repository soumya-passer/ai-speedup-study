def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    out = []
    ap = out.append
    for x in xs:
        if x < 0:
            t = int(-x * 1000 + 1e-6)
            ap(-((t + 5) // 10) / 100)
        else:
            t = int(x * 1000 + 1e-6)
            ap(((t + 5) // 10) / 100)
    return out
