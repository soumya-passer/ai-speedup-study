def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    lines = []
    cur = []        # words on the current line
    cur_len = 0     # length of " ".join(cur), tracked to avoid re-joining
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > width:
            if cur:
                lines.append(" ".join(cur))
                cur = []
            start = 0
            while lw - start > width:
                lines.append(w[start:start + width])
                start += width
            w = w[start:]
            lw = len(w)
        if cur and cur_len + 1 + lw <= width:
            cur.append(w)
            cur_len += 1 + lw
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
            cur_len = lw
    if cur:
        lines.append(" ".join(cur))
    return lines
