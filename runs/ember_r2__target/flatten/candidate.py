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
    while stack:
        v = pop()
        tv = type(v)
        if tv is list or tv is tuple:
            extend(reversed(v))
        else:
            append(v)
    return out
