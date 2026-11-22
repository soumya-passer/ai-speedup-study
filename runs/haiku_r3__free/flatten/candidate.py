def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    out = []
    # One iterator per open list/tuple. Walk the top one; when a nested
    # list/tuple is found, push its iterator and resume later. This makes
    # a single pass over every item instead of one pass per depth level.
    stack = [iter(x)]
    while stack:
        for v in stack[-1]:
            t = type(v)
            if t is list or t is tuple:
                stack.append(iter(v))
                break
            out.append(v)
        else:
            stack.pop()
    return out
