from math import copysign


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    # n = price in 1/10000 units (exact for <= 4 decimals); the third
    # decimal digit decides the rounding, the fourth is ignored.
    return [
        copysign(((round(abs(x) * 10000) // 10 + 5) // 10) / 100, x)
        for x in map(float, xs)
    ]
