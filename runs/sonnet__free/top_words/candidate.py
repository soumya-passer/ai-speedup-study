import re
from collections import Counter

_WORD = re.compile("[a-z]+")


def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    counts = Counter(_WORD.findall(text.lower()))
    pairs = sorted(counts.items(), key=lambda p: (-p[1], p[0]))
    return pairs[:k]
