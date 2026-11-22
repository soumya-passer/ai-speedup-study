def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    words = [w for w in text.split(" ") if w]
    lines = []
    cur = []
    for w in words:
        while len(w) > width:
            if cur:
                lines.append(" ".join(cur))
                cur = []
            lines.append(w[:width])
            w = w[width:]
        candidate = cur + [w]
        if len(" ".join(candidate)) <= width:
            cur = candidate
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines
