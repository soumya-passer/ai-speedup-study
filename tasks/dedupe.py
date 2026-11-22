KIND = "control"
TRAP = "none - dict.fromkeys keeps order and is exact"
FUNC = "dedupe"
FLOAT_TOL = False

ORIGINAL = '''
def dedupe(items):
    """Remove repeats, keep the first time each item appears. Items are ints."""
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out
'''

GOOD = '''
def dedupe(items):
    return list(dict.fromkeys(items))
'''

BAD = None

TESTS = [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([],), [])]
BENCH_SRC = "import random\n_r = random.Random(7)\nARGS = ([_r.randint(0, 3000) for _ in range(4000)],)"


def gen(rng):
    span = rng.choice([3, 20, 1000])
    return ([rng.randint(-span, span) for _ in range(rng.randint(0, 40))],)


EDGES = [([],), ([1, 1, 1],), ([0, -0],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([r.randint(0, 3000) for _ in range(4000)],)
