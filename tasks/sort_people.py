KIND = "trap"
TRAP = "sorting then reversing flips the order of people with the same age"
FUNC = "sort_people"
FLOAT_TOL = False

ORIGINAL = '''
def sort_people(people):
    """people is a list of (name, age). Return a new list, oldest first.
    People with the same age keep their order from the input."""
    out = []
    for p in people:
        i = len(out)
        while i > 0 and out[i - 1][1] < p[1]:
            i -= 1
        out.insert(i, p)
    return out
'''

GOOD = '''
def sort_people(people):
    return sorted(people, key=lambda p: -p[1])
'''

BAD = '''
def sort_people(people):
    return sorted(people, key=lambda p: p[1])[::-1]
'''

TESTS = [(([("ann", 30), ("bob", 50), ("cy", 40)],), [("bob", 50), ("cy", 40), ("ann", 30)]),
         (([],), [])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "ARGS = ([('p%d' % i, _r.randint(0, 100000)) for i in range(4000)],)")


def gen(rng):
    span = rng.choice([2, 5, 1000])
    return ([("n%d" % i, rng.randint(0, span)) for i in range(rng.randint(0, 20))],)


EDGES = [([("a", 1), ("b", 1)],), ([("a", 2), ("b", 1), ("c", 2)],)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return ([("p%d" % i, r.randint(0, 100000)) for i in range(4000)],)
