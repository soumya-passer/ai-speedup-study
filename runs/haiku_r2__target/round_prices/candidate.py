def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    out = []
    append = out.append
    for x in xs:
        s = repr(float(x))
        neg = s[0] == "-"
        if neg:
            s = s[1:]
        whole, _dot, frac = s.partition(".")
        cents = int(whole + (frac + "00")[:2])
        if frac[2:3] >= "5":
            cents += 1
        value = cents / 100
        append(-value if neg else value)
    return out
