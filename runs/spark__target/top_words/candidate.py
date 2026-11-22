import re
from collections import Counter

_pat = re.compile('[a-z]+')

def top_words(text, k):
    """The k most common words. A word is a run of the letters a-z after
    lower-casing; every other character separates words.
    Ties: alphabetical order. Returns a list of (word, count)."""
    words = _pat.findall(text.lower())
    if not words:
        return []
    counts = Counter(words)
    # sort by (-count, word) using pure C tuple sort (no py key func)
    neg = [(-c, w) for w, c in counts.items()]
    neg.sort()
    if k is None:
        return [(w, -c) for c, w in neg]
    return [(w, -c) for c, w in neg[:k]]
