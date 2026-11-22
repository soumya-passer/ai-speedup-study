_cache = {}


def _loop(ys, nw, w):
    out = []
    ap = out.append
    for i in range(nw):
        total = 0.0
        for v in ys[i:i + w]:
            total += v
        ap(total / w)
    return out


def _make(w):
    vars_str = ",".join("a%d" % k for k in range(w))
    expr = "0.0" + "".join("+a%d" % k for k in range(w))
    src = (
        "def f(ys, nw, w):\n"
        "    out = []\n"
        "    ap = out.append\n"
        "    for i in range(nw):\n"
        "        " + vars_str + " = ys[i:i+w]\n"
        "        ap((" + expr + ") / w)\n"
        "    return out\n"
    )
    env = {}
    exec(src, env)
    return env["f"]


def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    ys = list(map(float, xs))
    nw = len(ys) - w + 1
    if nw <= 0:
        return []
    if w > 1000:
        return _loop(ys, nw, w)
    f = _cache.get(w)
    if f is None:
        try:
            f = _make(w)
        except Exception:
            return _loop(ys, nw, w)
        _cache[w] = f
    return f(ys, nw, w)
