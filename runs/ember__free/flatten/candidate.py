def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    stack = list(x)
    stack.reverse()
    result = []
    append = result.append
    pop = stack.pop
    extend = stack.extend
    while stack:
        v = pop()
        t = type(v)
        if t is list or t is tuple:
            extend(reversed(v))
        else:
            append(v)
    return result
