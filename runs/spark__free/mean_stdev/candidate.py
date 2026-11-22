from math import sqrt as _sqrt

def mean_stdev(xs):
    n = len(xs)
    if n == 0:
        raise ValueError("empty")
    m = sum(xs) / n
    s = 0.0
    for x in xs:
        s += x * x
    v = s / n - m * m
    if v <= 0.0:
        return (m, 0.0)
    return (m, _sqrt(v))
