def flatten(x):
    s = x[::-1]
    o = []
    ap = o.append
    ex = s.extend
    pp = s.pop
    typ = type
    L = list
    Tu = tuple
    rv = reversed
    while s:
        v = pp()
        t = typ(v)
        if t is L:
            ex(v[::-1])
        elif t is Tu:
            ex(rv(v))
        else:
            ap(v)
    return o
