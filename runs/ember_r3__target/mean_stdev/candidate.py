from math import fsum, sqrt


def mean_stdev(xs):
    """Mean and population standard deviation of a list of numbers.
    Raises ValueError on an empty list."""
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    if n == 1:
        return (float(xs[0]), 0.0)
    try:
        # Shift by the first element (exact for ints/Fractions, and
        # harmless for floats) so deviations stay small when all
        # values share a large offset.  Then use a two-pass algorithm
        # with fsum (exact partials in C): accurate for cancellation,
        # unlike the one-pass E[x^2]-mean^2 formula, and far faster
        # than exact Fraction arithmetic.
        shift = xs[0]
        ds = [x - shift for x in xs]
        mean_d = fsum(ds) / n
        var = fsum((d - mean_d) * (d - mean_d) for d in ds) / n
    except TypeError:
        # Fallback for exotic numeric types (e.g. Decimal) that
        # fsum cannot mix with.
        from fractions import Fraction

        exact = [Fraction(x) for x in xs]
        mean_f = sum(exact) / n
        var_f = sum((x - mean_f) ** 2 for x in exact) / n
        return (float(mean_f), float(var_f) ** 0.5)
    return (float(shift + mean_d), sqrt(var))
