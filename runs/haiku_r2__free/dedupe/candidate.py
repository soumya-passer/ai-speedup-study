def dedupe(items):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    seen = set()
    out = []
    add = seen.add
    append = out.append
    for x in items:
        if x not in seen:
            add(x)
            append(x)
    return out
