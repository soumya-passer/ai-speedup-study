def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    append = out.append
    stack = []
    push = stack.append
    pop = stack.pop
    it = iter(x)
    while True:
        for v in it:
            t = type(v)
            if t is list or t is tuple:
                push(it)
                it = iter(v)
                break
            else:
                append(v)
        else:
            if not stack:
                return out
            it = pop()
