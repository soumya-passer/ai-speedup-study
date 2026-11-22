import re
from collections import Counter

_FINDALL = re.compile(r"[a-z]+").findall


def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    low = text.lower()
    counts = Counter(low.split())
    if counts:
        # Fast path is valid iff every distinct split-token is ascii a-z.
        # Then all non-whitespace chars are a-z, so split == [a-z]+ runs.
        # Checking only distinct tokens (~1500 vs 30000) is cheap.
        # Otherwise fall back to the exact regex tokenisation.
        distinct = "".join(counts)
        if not (distinct.isascii() and distinct.isalpha()):
            counts = Counter(_FINDALL(low))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
