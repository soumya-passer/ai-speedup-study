import re
from collections import Counter

_WORD_RE = re.compile(r"[a-z]+")


def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    counts = Counter(_WORD_RE.findall(text.lower()))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
