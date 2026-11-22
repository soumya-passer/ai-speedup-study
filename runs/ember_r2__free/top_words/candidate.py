import re
from collections import Counter

_findall = re.compile(r"[a-z]+").findall


def top_words(text, k):
    raw_counts = Counter(text.split())
    counts = {}
    counts_get = counts.get
    findall = _findall
    for tok, cnt in raw_counts.items():
        if tok.isascii() and tok.isalpha():
            w = tok.lower()
            counts[w] = counts_get(w, 0) + cnt
        else:
            for w in findall(tok.lower()):
                counts[w] = counts_get(w, 0) + cnt
    pairs = [(-cnt, w) for w, cnt in counts.items()]
    pairs.sort()
    return [(w, -cnt) for cnt, w in pairs[:k]]
