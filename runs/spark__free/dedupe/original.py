def dedupe(items):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out
