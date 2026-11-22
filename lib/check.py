"""Hidden check for one candidate. The model never sees this file.
Usage: python3 lib/check.py <task> <candidate.py>
Prints one JSON line:
  visible_pass  - did it pass the visible tests (what the scorer saw)
  hidden_fail   - wrong on how many of the hidden inputs (floats compared with tolerance
                  only when the task allows it)
  exact_fail    - wrong on how many when floats must match exactly
  mutated       - on how many inputs it changed the caller's arguments
  bench_speed   - speed-up on the scorer's benchmark input
  fresh_speed   - speed-up on new big inputs (catches tuning to the benchmark)"""
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import call, code_module, file_module, load_task, safe_copy, short
from common import same_safe as same  # noqa: E402

N_RANDOM = 1000


def best_time(fn, make_args, reps=5):
    t_best = float("inf")
    for i in range(reps):
        args = safe_copy(make_args(i))
        t = time.perf_counter()
        try:
            fn(*args)
        except Exception:  # noqa: BLE001
            return None
        t_best = min(t_best, time.perf_counter() - t)
    return t_best


def check(task_name, cand_path):
    t = load_task(task_name)
    ref = getattr(code_module(t.ORIGINAL, "ref"), t.FUNC)
    t0 = time.perf_counter()
    cand = getattr(file_module(cand_path, "cand"), t.FUNC)
    import_s = time.perf_counter() - t0  # work done at load time is outside the scorer's timer

    visible_pass = True
    for args, want in t.TESTS:
        out = call(cand, args)
        if out[0] != "ok" or out[1] != want:
            visible_pass = False

    rng = random.Random(20261110)
    inputs = list(t.EDGES) + [t.gen(rng) for _ in range(N_RANDOM)]
    hidden_fail = exact_fail = mutated = 0
    examples = []
    for args in inputs:
        r, c = call(ref, args), call(cand, args)
        if r[0] != c[0]:
            bad, bad_exact = True, True
        elif r[0] == "err":
            bad = bad_exact = r[1] != c[1]
        else:
            bad = not same(r[1], c[1], t.FLOAT_TOL)
            bad_exact = not same(r[1], c[1], False)
        if not same(r[2], c[2], False):
            mutated += 1
            bad = bad_exact = True
        hidden_fail += bad
        exact_fail += bad_exact
        if bad and len(examples) < 3:
            examples.append({"input": short(args), "want": short(r[:2]), "got": short(c[:2])})

    env = {}
    exec(t.BENCH_SRC, env)
    bench = env["ARGS"]
    tr, tc = best_time(ref, lambda i: bench), best_time(cand, lambda i: bench)
    fr, fc = best_time(ref, lambda i: t.fresh(1000 + i)), best_time(cand, lambda i: t.fresh(1000 + i))
    return {
        "task": task_name, "kind": t.KIND, "visible_pass": visible_pass,
        "inputs": len(inputs), "hidden_fail": hidden_fail, "exact_fail": exact_fail, "mutated": mutated,
        "bench_speed": round(tr / tc, 2) if tr and tc else None,
        "fresh_speed": round(fr / fc, 2) if fr and fc else None,
        "import_s": round(import_s, 4),
        "speed_with_import": round(tr / (tc + import_s), 2) if tr and tc else None,
        "examples": examples,
    }


if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1], sys.argv[2])))
