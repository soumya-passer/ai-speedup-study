def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    stack = [iter(x)]
    while stack:
        for v in stack[-1]:
            if type(v) in (list, tuple):
                stack.append(iter(v))
                break
            out.append(v)
        else:
            stack.pop()
    return out
