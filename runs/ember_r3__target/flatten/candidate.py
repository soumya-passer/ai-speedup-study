def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    stack = list(x)
    stack.reverse()
    out = []
    out_append = out.append
    stack_pop = stack.pop
    stack_extend = stack.extend
    while stack:
        v = stack_pop()
        t = type(v)
        if t is list or t is tuple:
            stack_extend(reversed(v))
        else:
            out_append(v)
    return out
