def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    out = []
    append = out.append
    for x in xs:
        w, _, f = repr(float(x)).partition(".")
        f = (f + "000")[:3]
        if w[0] == "-":
            cents = int(w[1:]) * 100 + int(f[:2])
            if f[2] >= "5":
                cents += 1
            append(-(cents / 100))
        else:
            cents = int(w) * 100 + int(f[:2])
            if f[2] >= "5":
                cents += 1
            append(cents / 100)
    return out
