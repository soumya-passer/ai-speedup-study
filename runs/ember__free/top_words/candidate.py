import re
from collections import Counter

_WORD_RE = re.compile(r"[a-z]+")

# bytes translation table: A-Z -> a-z, a-z -> a-z, everything else -> space
_TRANS = bytes(
    (i + 32) if 65 <= i <= 90 else (i if 97 <= i <= 122 else 32)
    for i in range(256)
)


def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    try:
        data = text.encode("ascii")
    except UnicodeEncodeError:
        counts = Counter(_WORD_RE.findall(text.lower()))
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    # ASCII fast path: one C translate (lower + separator -> space),
    # one C split, and Counter's C _count_elements.
    counts = Counter(data.translate(_TRANS).split())
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    return [(w.decode("ascii"), c) for w, c in top]
