KIND = "trap"
TRAP = "Counter.most_common breaks ties by first seen, not alphabetically; \\w+ also matches digits, _ and letters like é"
FUNC = "top_words"
FLOAT_TOL = False

ORIGINAL = '''
def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    words = []
    cur = ""
    for ch in text.lower():
        if "a" <= ch <= "z":
            cur += ch
        else:
            if cur:
                words.append(cur)
            cur = ""
    if cur:
        words.append(cur)
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    pairs = list(counts.items())
    for i in range(len(pairs)):
        for j in range(len(pairs) - 1 - i):
            a, b = pairs[j], pairs[j + 1]
            if (b[1] > a[1]) or (b[1] == a[1] and b[0] < a[0]):
                pairs[j], pairs[j + 1] = b, a
    return pairs[:k]
'''

GOOD = '''
import re
from collections import Counter

_W = re.compile("[a-z]+")


def top_words(text, k):
    counts = Counter(_W.findall(text.lower()))
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]
'''

BAD = '''
import re
from collections import Counter


def top_words(text, k):
    return Counter(re.findall(r"\\w+", text.lower())).most_common(k)
'''

TESTS = [(("the cat and the hat", 1), [("the", 2)]), (("Hello hello WORLD", 2), [("hello", 2), ("world", 1)])]
BENCH_SRC = ("import random\n_r = random.Random(7)\n"
             "_v = [''.join(_r.choice('abcdefghij') for _ in range(_r.randint(2, 6))) for _ in range(1500)]\n"
             "ARGS = (' '.join(_r.choice(_v) for _ in range(30000)), 10)")

ALPH = "abcdefghijklmnopqrstuvwxyzABC   ,.!'-0123_éÉßñ"


def gen(rng):
    text = "".join(rng.choice(ALPH) for _ in range(rng.randint(0, 80)))
    return (text, rng.randint(0, 6))


EDGES = [("", 3), ("b a b a c", 2), ("café cafe", 2), ("x_1 x_2", 3), ("A a", 0)]


def fresh(seed):
    import random
    r = random.Random(seed)
    v = ["".join(r.choice("abcdefghij") for _ in range(r.randint(2, 6))) for _ in range(1500)]
    return (" ".join(r.choice(v) for _ in range(30000)), 10)
