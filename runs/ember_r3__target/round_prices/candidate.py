def round_prices(xs):
    """Round each price to 2 decimal places, as written in decimal.
    A third decimal digit of 5 or more rounds away from zero:
    2.675 -> 2.68, -2.675 -> -2.68, 0.125 -> 0.13. Returns floats.
    Prices are under 1,000,000 with at most 4 decimal places."""
    xs = list(xs)
    try:
        # Inputs are floats/ints whose decimal value has <= 4 places, so
        # x*100 is within ~1e-8 of a multiple of 0.01 (in cents). Adding
        # 0.500001 (half a cent plus a tiny epsilon covering the binary
        # representation error) and truncating toward zero therefore
        # rounds half away from zero exactly as the decimal parsing did.
        return [int(x * 100 + (0.500001 if x >= 0 else -0.500001)) / 100
                for x in xs]
    except TypeError:
        # e.g. str/Decimal/Fraction inputs, which the original handled
        # via float(x); convert first, then use the same arithmetic.
        return [int(y * 100 + (0.500001 if y >= 0 else -0.500001)) / 100
                for x in xs for y in (float(x),)]
