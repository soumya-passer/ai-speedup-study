"""Shared helpers: load a task, load code from a string or file, compare results."""
import copy
import importlib.util
import math
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
TASKS_DIR = os.path.join(os.path.dirname(HERE), "tasks")
TASK_NAMES = sorted(f[:-3] for f in os.listdir(TASKS_DIR) if f.endswith(".py"))
REL_TOL = 1e-6


def load_task(name):
    spec = importlib.util.spec_from_file_location("task_" + name, os.path.join(TASKS_DIR, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def code_module(src, name):
    m = types.ModuleType(name)
    exec(compile(src, name, "exec"), m.__dict__)
    return m


def file_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def safe_copy(v):
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 50000))
    try:
        return copy.deepcopy(v)
    finally:
        sys.setrecursionlimit(old)


def same(a, b, tol):
    """Equal, or for floats (when tol) close within REL_TOL."""
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return type(a) is type(b) and len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if tol and isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=REL_TOL, abs_tol=1e-9)
    return a == b


def call(fn, args):
    """Run fn on a copy of args. Returns (outcome, value, args_after)."""
    a = safe_copy(args)
    try:
        return ("ok", fn(*a), a)
    except RecursionError:
        return ("err", "RecursionError", a)
    except Exception as e:  # noqa: BLE001
        return ("err", type(e).__name__, a)


def short(v, n=140):
    try:
        s = repr(v)
    except RecursionError:
        s = "<too deep to show>"
    return s if len(s) <= n else s[:n] + "..."


def same_safe(a, b, tol):
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 50000))
    try:
        return same(a, b, tol)
    finally:
        sys.setrecursionlimit(old)
