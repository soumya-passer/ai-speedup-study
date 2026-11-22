import re


def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    counts = {}
    for w in re.findall(r"[a-z]+", text.lower()):
        counts[w] = counts.get(w, 0) + 1
    pairs = sorted(counts.items(), key=lambda p: (-p[1], p[0]))
    return pairs[:k]
