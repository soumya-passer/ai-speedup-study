KIND = "trap"
TRAP = "textwrap.wrap splits at hyphens, turns tabs and new lines into spaces, and fills long words differently"
FUNC = "word_wrap"
FLOAT_TOL = False

ORIGINAL = '''
def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    words = [w for w in text.split(" ") if w]
    lines = []
    cur = []
    for w in words:
        while len(w) > width:
            if cur:
                lines.append(" ".join(cur))
                cur = []
            lines.append(w[:width])
            w = w[width:]
        candidate = cur + [w]
        if len(" ".join(candidate)) <= width:
            cur = candidate
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines
'''

GOOD = '''
def word_wrap(text, width):
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    cur = []
    n = 0
    for w in text.split(" "):
        if not w:
            continue
        while len(w) > width:
            if cur:
                lines.append(" ".join(cur))
                cur = []
                n = 0
            lines.append(w[:width])
            w = w[width:]
        add = len(w) if not cur else n + 1 + len(w)
        if add <= width:
            cur.append(w)
            n = add
        else:
            lines.append(" ".join(cur))
            cur = [w]
            n = len(w)
    if cur:
        lines.append(" ".join(cur))
    return lines
'''

BAD = '''
import textwrap


def word_wrap(text, width):
    if width < 1:
        raise ValueError("width < 1")
    return textwrap.wrap(text, width)
'''

TESTS = [(("the quick brown fox", 10), ["the quick", "brown fox"]), (("a b c", 1), ["a", "b", "c"])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "ARGS = (' '.join(''.join(_r.choice('abcdefgh') for _ in range(_r.randint(1, 8))) for _ in range(20000)), 400)")

ALPH = "abcde     -\t\n"


def gen(rng):
    return ("".join(rng.choice(ALPH) for _ in range(rng.randint(0, 50))), rng.randint(0, 9))


EDGES = [("", 5), ("well-known fact", 6), ("abcdefghij", 4), ("a\tb c", 3), ("ab abcdefg", 4)]


def fresh(seed):
    import random
    r = random.Random(seed)
    return (" ".join("".join(r.choice("abcdefgh") for _ in range(r.randint(1, 8))) for _ in range(20000)), 400)
