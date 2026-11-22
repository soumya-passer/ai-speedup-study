"""Check the checker. For every task:
  original - must show 0 fails and about 1.0x
  good     - a correct fast version: must show 0 fails (no false alarms) and pass visible tests
  bad      - the trap version: must PASS the visible tests but FAIL the hidden check
Writes results/validation.json and prints a table."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import check  # noqa: E402
from common import TASK_NAMES, load_task  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
only = sys.argv[1:] or TASK_NAMES
rows = []
tmp = tempfile.mkdtemp(dir=os.path.join(ROOT, ".tmp")) if os.path.isdir(os.path.join(ROOT, ".tmp")) else tempfile.mkdtemp()
for name in only:
    t = load_task(name)
    for label, src in (("original", t.ORIGINAL), ("good", t.GOOD), ("bad", t.BAD)):
        if src is None:
            continue
        path = os.path.join(tmp, "%s_%s.py" % (name, label))
        with open(path, "w") as f:
            f.write(src)
        r = check(name, path)
        r["version"] = label
        rows.append(r)
        print("%-15s %-8s visible=%-5s hidden_fail=%-4d exact_fail=%-4d mutated=%-3d bench=%-7s fresh=%s" % (
            name, label, r["visible_pass"], r["hidden_fail"], r["exact_fail"], r["mutated"],
            r["bench_speed"], r["fresh_speed"]), flush=True)

os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
with open(os.path.join(ROOT, "results", "validation.json"), "w") as f:
    json.dump(rows, f, indent=1)
