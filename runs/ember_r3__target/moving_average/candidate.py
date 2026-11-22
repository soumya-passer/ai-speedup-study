def moving_average(xs, w):
    """Average of each window of w numbers in a row.
    Results must be bit-for-bit identical to this function: each window is
    added left to right, starting from 0.0, then divided by w.
    Returns [] when w > len(xs). Raises ValueError when w < 1."""
    if w < 1:
        raise ValueError("w < 1")
    n = len(xs)
    if w > n:
        return []
    # Convert once, in order (same float() calls' values as the original
    # for deterministic inputs). float(x) * 1.0 == float(x) exactly for
    # every float, so omitting the *1.0 does not change any bit.
    ys = list(map(float, xs))
    n_out = n - w + 1

    # Small total work, non-int w (let range() raise as in the original),
    # or very large w: use a plain slice loop (still avoids the original's
    # per-element float()/range()/indexing, and sums in the same order).
    if not isinstance(w, int) or w > 1000 or w * n_out < 50000:
        out = []
        ap = out.append
        W = w
        for i in range(n_out):
            total = 0.0
            for x in ys[i:i + W]:
                total = total + x
            ap(total / W)
        return out

    # Large work, moderate w: run a cached, generated function in which
    # each window's elements are unpacked into locals and summed with a
    # single left-to-right expression 0.0+a0+a1+...+a(w-1). This is
    # bit-for-bit the same sequence of additions as the original nested
    # loop, but with no inner loop / indexing / float() per element.
    fn = _cache.get(w)
    if fn is None:
        params = ",".join("a%d" % k for k in range(w))
        expr = "+".join("a%d" % k for k in range(w))
        src = (
            "def _run(ys, n_out, w):\n"
            "    out = []\n"
            "    ap = out.append\n"
            "    for i in range(n_out):\n"
            "        %s = ys[i:i+w]\n"
            "        ap((0.0+%s)/w)\n"
            "    return out\n" % (params, expr)
        )
        ns = {}
        exec(src, {}, ns)
        fn = ns["_run"]
        _cache[w] = fn
    return fn(ys, n_out, w)


_cache = {}
