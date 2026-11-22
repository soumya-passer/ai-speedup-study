import re
from collections import Counter
from heapq import nsmallest

_WORD_RE = re.compile(r"[a-z]+")


def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    # Lower-casing in C preserves the exact original semantics (including
    # Unicode lower-casing); the regex scan and Counter are also C-accelerated.
    counts = Counter(_WORD_RE.findall(text.lower()))
    if k < 0:
        # Preserve original pairs[:k] behaviour for negative k.
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    # nsmallest is O(n log k) and ideal for the usual small k; fall back to
    # a full (C) sort when k is large relative to the vocabulary.
    if k < len(counts) and k < 128:
        return nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
