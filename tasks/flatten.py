KIND = "trap"
TRAP = "a recursive rewrite crashes on deep nesting (RecursionError); a generic iterable check splits strings"
FUNC = "flatten"
FLOAT_TOL = False

ORIGINAL = '''
def flatten(x):
    """x is a list. Lists and tuples inside it, at any depth (even 5,000
    levels), are opened up. Everything else - numbers, strings, bytes,
    dicts - is kept as one item. Returns a new flat list, in order."""
    items = list(x)
    while any(type(v) in (list, tuple) for v in items):
        nxt = []
        for v in items:
            if type(v) in (list, tuple):
                nxt.extend(v)
            else:
                nxt.append(v)
        items = nxt
    return items
'''

GOOD = '''
def flatten(x):
    out = []
    stack = [iter(x)]
    while stack:
        for v in stack[-1]:
            if type(v) in (list, tuple):
                stack.append(iter(v))
                break
            out.append(v)
        else:
            stack.pop()
    return out
'''

BAD = '''
def flatten(x):
    out = []
    for v in x:
        if isinstance(v, (list, tuple)):
            out.extend(flatten(v))
        else:
            out.append(v)
    return out
'''

TESTS = [(([1, [2, [3]], (4, 5)],), [1, 2, 3, 4, 5]), ((["ab", ["c"]],), ["ab", "c"])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "_spine = [0]\n"
             "for _i in range(400):\n"
             "    _spine = [_r.randint(0, 9), _spine]\n"
             "ARGS = ([_r.randint(0, 9) for _ in range(5000)] + [_spine],)")


def gen(rng):
    def mk(d):
        k = rng.random()
        if d == 0 or k < 0.4:
            return rng.choice([1, 2.5, "ab", b"x", {"k": 1}, None, ""])
        return rng.choice([list, tuple])(mk(d - 1) for _ in range(rng.randint(0, 3)))
    return ([mk(rng.randint(0, 6)) for _ in range(rng.randint(0, 5))],)


def _deep(n):
    v = [1]
    for _ in range(n):
        v = [v]
    return v


EDGES = [([],), ([[], ()],), (["abc"],), ([_deep(1500)],), ([_deep(5000)],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    spine = [0]
    for _ in range(400):
        spine = [r.randint(0, 9), spine]
    return ([r.randint(0, 9) for _ in range(5000)] + [spine],)
