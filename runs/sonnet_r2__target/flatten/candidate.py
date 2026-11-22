def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    append = out.append
    stack = [iter(x)]
    push = stack.append
    pop = stack.pop
    while stack:
        for v in stack[-1]:
            t = type(v)
            if t is list or t is tuple:
                push(iter(v))
                break
            append(v)
        else:
            pop()
    return out
