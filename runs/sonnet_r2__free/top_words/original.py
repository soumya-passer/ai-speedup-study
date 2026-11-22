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
