"""Scorer for one task. Usage: python3 score.py
Runs the visible tests on candidate.py, then times candidate.py against
original.py on the benchmark input (best of 5 runs)."""
import copy
import importlib.util
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FUNC = 'dedupe'
TESTS = [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([],), [])]
BENCH_SRC = 'import random\n_r = random.Random(7)\nARGS = ([_r.randint(0, 3000) for _ in range(4000)],)'
TARGET = 2.0  # None means no speed target


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return getattr(m, FUNC)


def best(fn, args, reps=5):
    t_best = float("inf")
    for _ in range(reps):
        a = copy.deepcopy(args)
        t = time.perf_counter()
        fn(*a)
        t_best = min(t_best, time.perf_counter() - t)
    return t_best


ref, cand = load("original"), load("candidate")
ok = True
for args, want in TESTS:
    try:
        got = cand(*copy.deepcopy(args))
    except Exception as e:  # noqa: BLE001
        got = "raised " + type(e).__name__
    if got != want:
        ok = False
        print("FAIL %s%r: want %r, got %r" % (FUNC, args, want, got))
if ok:
    print("tests: all %d passed" % len(TESTS))

env = {}
exec(BENCH_SRC, env)
speed = best(ref, env["ARGS"]) / best(cand, env["ARGS"])
print("speed: %.2fx faster than original" % speed)

if TARGET is not None and speed < TARGET:
    ok = False
    print("speed is below the %.1fx target" % TARGET)
print("ACCEPTED" if ok else "NOT ACCEPTED")
