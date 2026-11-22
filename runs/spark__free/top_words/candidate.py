import re
from collections import Counter
from heapq import nsmallest

_findall = re.compile('[a-z]+').findall

def top_words(text, k):
    counts = Counter(_findall(text.lower()))
    if not counts:
        return []
    if k is not None and 0 < k < len(counts) and k * 8 < len(counts):
        top = nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return top
    dec = [(-c, w) for w, c in counts.items()]
    dec.sort()
    return [(w, -v) for v, w in dec[:k]]
