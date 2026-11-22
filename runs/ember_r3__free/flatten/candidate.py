def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    stack = list(x)
    stack.reverse()
    pop = stack.pop
    extend = stack.extend
    append = out.append
    _type = type
    while stack:
        v = pop()
        t = _type(v)
        if t is list or t is tuple:
            extend(reversed(v))
        else:
            append(v)
    return out
