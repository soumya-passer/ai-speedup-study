from math import copysign


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    # Inputs have at most 4 decimals, so abs(x) * 10000 is within 1e-5 of an
    # integer; +0.5 and int() recover it exactly. The 4th digit is dropped
    # (//10) and the 3rd digit decides rounding ((t + 5) // 10).
    return [
        copysign(((int(abs(x) * 10000 + 0.5) // 10 + 5) // 10) / 100, x)
        for x in xs
    ]
