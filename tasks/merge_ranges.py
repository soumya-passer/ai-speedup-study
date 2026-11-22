KIND = "trap"
TRAP = "using < instead of <= leaves ranges that only touch, like (1,3) and (3,5), unmerged"
FUNC = "merge_ranges"
FLOAT_TOL = False

ORIGINAL = '''
def merge_ranges(ranges):
    """ranges is a list of (start, end) int pairs, start <= end, both ends
    included. Merge ranges that overlap or share an end point, so (1, 3) and
    (3, 5) become (1, 5), but (1, 3) and (4, 5) stay apart.
    Return the merged ranges as tuples, sorted by start."""
    rs = [tuple(r) for r in ranges]
    changed = True
    while changed:
        changed = False
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, b = rs[i], rs[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    rs[i] = (min(a[0], b[0]), max(a[1], b[1]))
                    del rs[j]
                    changed = True
                    break
            if changed:
                break
    return sorted(rs)
'''

GOOD = '''
def merge_ranges(ranges):
    out = []
    for s, e in sorted(tuple(r) for r in ranges):
        if out and s <= out[-1][1]:
            if e > out[-1][1]:
                out[-1] = (out[-1][0], e)
        else:
            out.append((s, e))
    return out
'''

BAD = '''
def merge_ranges(ranges):
    out = []
    for s, e in sorted(tuple(r) for r in ranges):
        if out and s < out[-1][1]:
            out[-1] = (out[-1][0], max(e, out[-1][1]))
        else:
            out.append((s, e))
    return out
'''

TESTS = [(([(1, 3), (2, 6), (8, 10)],), [(1, 6), (8, 10)]), (([(5, 7), (1, 2)],), [(1, 2), (5, 7)])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "_s = [_r.randint(0, 10 ** 7) for _ in range(600)]\n"
             "ARGS = ([(s, s + _r.randint(0, 50)) for s in _s],)")


def gen(rng):
    out = []
    for _ in range(rng.randint(0, 10)):
        s = rng.randint(0, 20)
        out.append((s, s + rng.randint(0, 4)))
    return (out,)


EDGES = [([],), ([(1, 3), (3, 5)],), ([(1, 3), (4, 5)],), ([(1, 1), (1, 1)],), ([(1, 10), (2, 3)],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    s = [r.randint(0, 10 ** 7) for _ in range(600)]
    return ([(x, x + r.randint(0, 50)) for x in s],)
