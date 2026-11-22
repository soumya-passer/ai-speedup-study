def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    try:
        return [int(x * 100 + 0.500001 if x >= 0 else x * 100 - 0.500001) / 100 for x in xs]
    except TypeError:
        out = []
        append = out.append
        for x in xs:
            f = float(x)
            append(int(f * 100 + 0.500001 if f >= 0 else f * 100 - 0.500001) / 100)
        return out
