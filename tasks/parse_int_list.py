KIND = "trap"
TRAP = "int() accepts '1_000', '٣' and tabs, and split(',') breaks on empty items like '1,,2'"
FUNC = "parse_int_list"
FLOAT_TOL = False

ORIGINAL = '''
def parse_int_list(s):
    """Parse comma-separated whole numbers, like "1, -2,+3".
    Each item may have spaces (only the space character) around it.
    Empty items are skipped: "1,,2," gives [1, 2].
    An item is an optional + or - and then one or more of the digits 0-9.
    Anything else raises ValueError."""
    out = []
    for item in s.split(","):
        i, j = 0, len(item)
        while i < j and item[i] == " ":
            i += 1
        while j > i and item[j - 1] == " ":
            j -= 1
        if i == j:
            continue
        sign = 1
        if item[i] in "+-":
            if item[i] == "-":
                sign = -1
            i += 1
        if i == j:
            raise ValueError("bad item")
        value = 0
        while i < j:
            ch = item[i]
            if ch not in "0123456789":
                raise ValueError("bad item")
            value = value * 10 + (ord(ch) - 48)
            i += 1
        out.append(sign * value)
    return out
'''

GOOD = '''
import re

_OK = re.compile(r"[+-]?[0-9]+")


def parse_int_list(s):
    out = []
    for item in s.split(","):
        t = item.strip(" ")
        if not t:
            continue
        if not _OK.fullmatch(t):
            raise ValueError("bad item")
        out.append(int(t))
    return out
'''

BAD = '''
def parse_int_list(s):
    return [int(p) for p in s.split(",") if p.strip()]
'''

TESTS = [(("1, -2,+3",), [1, -2, 3]), (("42",), [42])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "ARGS = (','.join(' %d ' % _r.randint(-10 ** 9, 10 ** 9) for _ in range(30000)),)")

ITEMS = ["1", "-2", "+3", " 4 ", "", " ", "1_000", "٣", "\t5", "5\t", "+", "-", "x", "007", "12a", "  -0 ", "1 2"]


def gen(rng):
    return (",".join(rng.choice(ITEMS) for _ in range(rng.randint(0, 6))),)


EDGES = [("",), ("1,,2,",), ("1_000",), ("٣",), ("\t5",), (" + 5",), (",",)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return (",".join(" %d " % r.randint(-10 ** 9, 10 ** 9) for _ in range(30000)),)
