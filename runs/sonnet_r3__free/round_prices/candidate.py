from math import copysign


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    # With at most 4 decimals, abs(x) * 10000 is within float noise of an
    # integer, so +0.5 and int() recover the exact 4-decimal digits.
    return [copysign((int(abs(x) * 10000 + 0.5) + 50) // 100 / 100, x) for x in xs]
