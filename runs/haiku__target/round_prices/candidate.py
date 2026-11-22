from itertools import repeat


def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    # float() and repr() run in C via map(); the comprehension does the integer work.
    # n is the first three decimal digits as one signed integer, e.g. "-2" + "675" -> -2675.
    # Adding 5 and dividing by 10 rounds the digit pair away from zero (2.675 -> 268 cents).
    return [
        -(((5 - n) // 10) / 100) if ip[0] == "-" else ((n + 5) // 10) / 100
        for ip, _, fp in map(str.partition, map(repr, map(float, xs)), repeat("."))
        for n in (int(ip + (fp + "000")[:3]),)
    ]
