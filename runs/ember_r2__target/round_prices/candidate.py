def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    return [-(int(abs(y) * 100 + 0.500001) / 100) if y < 0 else int(abs(y) * 100 + 0.500001) / 100 for y in map(float, xs)]
