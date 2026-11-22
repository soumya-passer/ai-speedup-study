def dedupe(items):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    return list(dict.fromkeys(items))
