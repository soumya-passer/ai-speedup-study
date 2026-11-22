from math import copysign


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    # Each price is an integer count of 1e-4 units after round(x * 10000).
    # Adding 50 and taking hundreds gives half-up rounding to cents on the
    # magnitude, which matches the third decimal digit rule.
    return [
        copysign((abs(round(float(x) * 10000)) + 50) // 100 / 100, x)
        for x in xs
    ]
