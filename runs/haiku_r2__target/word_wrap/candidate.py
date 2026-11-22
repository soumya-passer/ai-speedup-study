def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    cur = []
    cur_len = 0  # length of " ".join(cur)
    for w in text.split(" "):
        if not w:
            continue
        n = len(w)
        if n > width:
            if cur:
                lines.append(" ".join(cur))
                cur = []
                cur_len = 0
            i = 0
            while n - i > width:
                lines.append(w[i:i + width])
                i += width
            w = w[i:]
            n = len(w)
        if cur and cur_len + 1 + n <= width:
            cur.append(w)
            cur_len += 1 + n
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
            cur_len = n
    if cur:
        lines.append(" ".join(cur))
    return lines
