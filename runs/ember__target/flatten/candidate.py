def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    out_append = out.append
    stack = [iter(x)]
    stack_append = stack.append
    stack_pop = stack.pop
    while stack:
        it = stack_pop()
        for v in it:
            t = type(v)
            if t is list or t is tuple:
                stack_append(it)
                stack_append(iter(v))
                break
            out_append(v)
    return out
