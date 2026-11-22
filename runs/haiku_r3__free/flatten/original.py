def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    items = list(x)
    while any(type(v) in (list, tuple) for v in items):
        nxt = []
        for v in items:
            if type(v) in (list, tuple):
                nxt.extend(v)
            else:
                nxt.append(v)
        items = nxt
    return items
