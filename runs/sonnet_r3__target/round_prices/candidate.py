from math import copysign


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    out = []
    append = out.append
    for x in xs:
        x = float(x)
        if x < 0:
            append(-((int(-x * 10000 + 0.5) + 50) // 100 / 100))
        elif x == 0 and copysign(1.0, x) < 0:
            append(-0.0)
        else:
            append((int(x * 10000 + 0.5) + 50) // 100 / 100)
    return out
