def flatten(x):
    k = 0
    for v in x:
        t = type(v)
        if t is list or t is tuple:
            break
        k += 1
    else:
        return list(x)
    res = x[:k]
    app = res.append
    stack = x[k:]
    stack.reverse()
    pop = stack.pop
    push = stack.append
    extend = stack.extend
    v = pop()
    while 1:
        t = type(v)
        if t is list or t is tuple:
            n = len(v)
            if n:
                if n == 1:
                    v = v[0]
                    continue
                if n == 2:
                    push(v[1])
                else:
                    extend(v[:0:-1])
                v = v[0]
                continue
        else:
            app(v)
        if stack:
            v = pop()
        else:
            return res
