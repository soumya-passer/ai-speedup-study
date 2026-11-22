def flatten(x):
    out = []
    a = out.append
    s = x[::-1]
    p = s.pop
    e = s.extend
    typ = type
    lst = list
    tpl = tuple
    while s:
        v = p()
        t = typ(v)
        if t is lst:
            e(v[::-1])
        elif t is tpl:
            e(v[::-1])
        else:
            a(v)
    return out
