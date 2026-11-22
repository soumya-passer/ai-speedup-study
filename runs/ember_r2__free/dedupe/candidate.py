def dedupe(items, _fromkeys=dict.fromkeys, _list=list):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    try:
        return _list(_fromkeys(items))
    except TypeError:
        out = []
        for x in items:
            if x not in out:
                out.append(x)
        return out
