from math import sumprod as _sp, sqrt as _sq, fsum as _fs

def mean_stdev(xs, _len=len, _sum=sum, _sp=_sp, _sq=_sq):
    n = _len(xs)
    if n == 0:
        raise ValueError("empty")
    r = 1.0 / n
    m = _sum(xs) * r
    mm = m * m
    v = _sp(xs, xs) * r - mm
    if v >= mm * 1e-9:
        return (m, _sq(v))
    vv = _fs((x - m) * (x - m) for x in xs) * r
    if vv <= 0.0:
        return (m, 0.0)
    return (m, _sq(vv))
