def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    return [(((int(abs(x) * 10000 + 0.5) + 50) // 100) * (-1 if x < 0 else 1)) / 100 for x in xs]
