import re


def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")

    # Fast path (all work in C): valid when internal separators are single
    # spaces.  Stripping outer spaces makes the stripped text exactly the
    # words joined by single spaces.  A greedy regex match of up to width
    # chars ending at a word boundary is then exactly the maximal prefix
    # of words fitting in width, i.e. one output line.
    # Words longer than width, or any other mismatch, make the
    # reconstructed text differ from the stripped text, in which case we
    # fall through to the general loop below.
    if isinstance(width, int) and width <= 100000 and "  " not in text:
        stripped = text.strip(" ")
        if not stripped:
            return []
        lines = re.findall(
            r"(?s)[^ ].{0,%d}(?=(?: [^ ])|\Z)" % (width - 1), stripped
        )
        if " ".join(lines) == stripped:
            return lines

    # General path: track the current line length instead of joining a
    # candidate list for every word, and join each line only once.
    lines = []
    lines_append = lines.append
    cur = []
    cur_len = 0
    for w in text.split(" "):
        if not w:
            continue
        lw = len(w)
        if lw > width:
            if cur:
                lines_append(" ".join(cur))
                cur = []
                cur_len = 0
            start = 0
            while lw - start > width:
                lines_append(w[start:start + width])
                start += width
            if start:
                w = w[start:]
                lw -= start
        if cur:
            if cur_len + 1 + lw <= width:
                cur.append(w)
                cur_len += 1 + lw
            else:
                lines_append(" ".join(cur))
                cur = [w]
                cur_len = lw
        else:
            cur = [w]
            cur_len = lw
    if cur:
        lines_append(" ".join(cur))
    return lines
