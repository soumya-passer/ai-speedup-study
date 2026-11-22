"""Print failures, load-time tricks, and the summary table from results/runs.json."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, "results", "runs.json")))

print("--- failed the hidden check")
for r in rows:
    if r.get("hidden_fail"):
        print(r["group"], r["task"], r["kind"], r["hidden_fail"], "|", r["examples"][0])
print("--- heavy work at load time (import_s > 0.005)")
for r in rows:
    if r.get("import_s", 0) > 0.005:
        print(r["group"], r["task"], r["import_s"], "bench", r.get("bench_speed"), "with load", r.get("speed_with_import"))
print("--- summary: group, runs, accepted, hidden fails, trap fails, control fails")
for g in sorted({r["group"] for r in rows}):
    rs = [r for r in rows if r["group"] == g]
    print(g, len(rs), sum(r["accepted"] for r in rs), sum(bool(r.get("hidden_fail")) for r in rs),
          sum(bool(r.get("hidden_fail")) and r["kind"] == "trap" for r in rs),
          sum(bool(r.get("hidden_fail")) and r["kind"] == "control" for r in rs),
          "accepted-but-wrong", sum(bool(r.get("hidden_fail")) and r["accepted"] for r in rs))
