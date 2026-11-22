def dedupe(items):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    out = []
    seen = set()
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
