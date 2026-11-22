from bisect import bisect_right
from itertools import accumulate, repeat
from operator import add


def word_wrap(text, width):
    """Greedy wrap. Words are separated only by the space character; tabs,
    new lines and hyphens are part of a word. Each line holds as many words
    as fit within width, joined by one space. A word longer than width is
    cut into pieces of width characters, each on its own line, and the last
    piece starts the next line. Raises ValueError when width < 1."""
    if width < 1:
        raise ValueError("width < 1")
    if not text:
        return []
    # Fast path for normalised text: no leading/trailing space and no
    # double space, so words are exactly the substrings between single
    # spaces and a line is a substring of text.  The greedy line starting
    # at pos ends at the last space at index <= pos+width; if there is
    # none, the word starting at pos is longer than width and is cut.
    if text[0] != " " and text[-1] != " " and "  " not in text:
        lines = []
        lines_append = lines.append
        rfind = text.rfind
        n = len(text)
        pos = 0
        while pos < n:
            if n - pos <= width:
                lines_append(text[pos:])
                break
            e = rfind(" ", pos, pos + width + 1)
            if e == -1:
                lines_append(text[pos:pos + width])
                pos += width
            else:
                lines_append(text[pos:e])
                pos = e + 1
        return lines
    # Generic path (irregular spacing).
    words = list(filter(None, text.split(" ")))
    if not words:
        return []
    lens = list(map(len, words))
    if max(lens) > width:
        # Fallback for over-long words: per-word loop tracking cur length
        # (no repeated join / list copy like the original).
        lines = []
        lines_append = lines.append
        join = " ".join
        cur = []
        cur_append = cur.append
        cur_len = 0
        for w, lw in zip(words, lens):
            if lw > width:
                while lw > width:
                    if cur:
                        lines_append(join(cur))
                        cur = []
                        cur_append = cur.append
                        cur_len = 0
                    lines_append(w[:width])
                    w = w[width:]
                    lw -= width
            if cur:
                new_len = cur_len + 1 + lw
                if new_len <= width:
                    cur_append(w)
                    cur_len = new_len
                else:
                    lines_append(join(cur))
                    cur = [w]
                    cur_append = cur.append
                    cur_len = lw
            else:
                cur_append(w)
                cur_len = lw
        if cur:
            lines_append(join(cur))
        return lines
    # Fast path (all words fit): q[k] = sum(len+1 for first k words).
    # A line words[start:end] fits iff q[end] - q[start] <= width + 1,
    # and q is increasing, so the maximal end is found by C bisect.
    q = list(accumulate(map(add, lens, repeat(1)), initial=0))
    lines = []
    lines_append = lines.append
    join = " ".join
    n = len(words)
    n1 = n + 1
    limit_offset = width + 1
    start = 0
    br = bisect_right
    while start < n:
        end = br(q, q[start] + limit_offset, start + 1, n1) - 1
        lines_append(join(words[start:end]))
        start = end
    return lines
