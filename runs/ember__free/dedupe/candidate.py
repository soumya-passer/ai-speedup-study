def dedupe(items):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    try:
        return list(dict.fromkeys(items))
    except TypeError:
        out = []
        for x in items:
            if x not in out:
                out.append(x)
        return out
