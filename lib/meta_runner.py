"""Run one Meta model on every task, in a loop with 3 tools, like the Claude helpers.
Usage: python3 lib/meta_runner.py <ember|spark> [task ...]
Needs MODEL_API_KEY in the environment (set it in your own terminal; never in a file).
Logs every call's tokens and cost to results/meta_usage.jsonl and stops before the cost cap."""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TASK_NAMES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://api.meta.ai/v1"
MODELS = {  # USD per 1M tokens: input, output (from dev.meta.ai/platform/models, 2026-11-10)
    "ember": ("muse-ember-1.0", 0.10, 0.50),
    "spark": ("muse-spark-1.3", 1.25, 4.25),
}
for _k in ("ember", "spark"):  # repeat runs use their own folders, same model
    for _r in ("r2", "r3"):
        MODELS["%s_%s" % (_k, _r)] = MODELS[_k]
COST_CAP_USD = float(os.environ.get("META_COST_CAP_USD", "12"))
MAX_TURNS = 25
MAX_SCORER_RUNS = 5
USAGE = os.path.join(ROOT, "results", "meta_usage.jsonl")
ERRORS = os.path.join(ROOT, "results", "meta_errors.jsonl")  # every timeout, HTTP error and stop
CONTEXT = {}  # model key, setup and task of the run in progress

TOOLS = [
    {"type": "function", "function": {
        "name": "read_file", "description": "Read a file in your work folder.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string", "enum": ["original.py", "candidate.py", "score.py"]}}, "required": ["name"]}}},
    {"type": "function", "function": {
        "name": "write_candidate", "description": "Replace the whole of candidate.py with this text.",
        "parameters": {"type": "object", "properties": {"content": {"type": "string"}}, "required": ["content"]}}},
    {"type": "function", "function": {
        "name": "run_scorer", "description": "Run score.py on candidate.py and return its output.",
        "parameters": {"type": "object", "properties": {}}}},
]


def spent():
    if not os.path.exists(USAGE):
        return 0.0
    return sum(json.loads(line)["usd"] for line in open(USAGE))


def log_error(kind, detail):
    os.makedirs(os.path.dirname(ERRORS), exist_ok=True)
    with open(ERRORS, "a") as f:
        f.write(json.dumps({"time": time.strftime("%Y-%m-%dT%H:%M:%S"), **CONTEXT,
                            "kind": kind, "detail": str(detail)[:200]}) + "\n")


def chat(model_id, messages):
    body = json.dumps({"model": model_id, "messages": messages, "tools": TOOLS}).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body, headers={
        "Authorization": "Bearer " + os.environ["MODEL_API_KEY"], "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            log_error("http_%s" % e.code, "attempt %d of 4" % (attempt + 1))
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            raise SystemExit("API error %s: %s" % (e.code, e.read()[:300]))
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            is_timeout = isinstance(e, TimeoutError) or "timed out" in str(e)
            log_error("timeout" if is_timeout else "network_error", "attempt %d of 4: %s" % (attempt + 1, e))
            if attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            raise


def run_task(key, setup, task):
    model_id, p_in, p_out = MODELS[key]
    folder = os.path.join(ROOT, "runs", "%s__%s" % (key, setup), task)
    CONTEXT.clear()
    CONTEXT.update(model=key, setup=setup, task=task)
    if os.path.exists(os.path.join(folder, "transcript.json")):
        print(key, setup, task, "already done, skipped", flush=True)
        return
    # unfinished run: start again from the original code
    with open(os.path.join(folder, "original.py")) as src, open(os.path.join(folder, "candidate.py"), "w") as dst:
        dst.write(src.read())
    prompt = open(os.path.join(ROOT, "prompts", "%s__%s__%s.txt" % (key, setup, task))).read()
    prompt = prompt.split("Run the scorer with exactly")[0] + (
        "Use the tools: read_file, write_candidate, run_scorer.\n"
        "Rules:\n- You may run the scorer up to 5 times.\n- Standard library only.\n"
        "- When done, reply with the last scorer output and 2 or 3 lines on what you changed.\n")
    messages = [{"role": "user", "content": prompt}]
    scorer_runs = 0
    for turn in range(MAX_TURNS):
        if spent() >= COST_CAP_USD:
            raise SystemExit("cost cap reached: $%.2f" % spent())
        resp = chat(model_id, messages)
        u = resp.get("usage", {})
        usd = u.get("prompt_tokens", 0) / 1e6 * p_in + u.get("completion_tokens", 0) / 1e6 * p_out
        with open(USAGE, "a") as f:
            f.write(json.dumps({"model": model_id, "setup": setup, "task": task, "turn": turn,
                                "in": u.get("prompt_tokens"), "out": u.get("completion_tokens"), "usd": usd}) + "\n")
        msg = resp["choices"][0]["message"]
        messages.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")})
        calls = msg.get("tool_calls") or []
        if not calls:
            break
        for c in calls:
            name = c["function"]["name"]
            try:
                args = json.loads(c["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            if name == "read_file" and args.get("name") in ("original.py", "candidate.py", "score.py"):
                out = open(os.path.join(folder, args["name"])).read()
            elif name == "write_candidate" and isinstance(args.get("content"), str):
                with open(os.path.join(folder, "candidate.py"), "w") as f:
                    f.write(args["content"])
                out = "candidate.py written"
            elif name == "run_scorer":
                if scorer_runs >= MAX_SCORER_RUNS:
                    out = "scorer limit reached (5 runs)"
                else:
                    scorer_runs += 1
                    p = subprocess.run([sys.executable, "-I", "score.py"], cwd=folder,
                                       capture_output=True, text=True, timeout=600)
                    out = (p.stdout + p.stderr)[-3000:]
            else:
                out = "unknown tool or bad arguments"
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": out})
    with open(os.path.join(folder, "transcript.json"), "w") as f:
        json.dump(messages, f, indent=1)
    print(key, setup, task, "turns=%d scorer_runs=%d spent=$%.3f" % (turn + 1, scorer_runs, spent()), flush=True)


if __name__ == "__main__":
    key = sys.argv[1]
    tasks = sys.argv[2:] or TASK_NAMES
    os.makedirs(os.path.dirname(USAGE), exist_ok=True)
    for setup in ("free", "target"):
        for task in tasks:
            try:
                run_task(key, setup, task)
            except BaseException as e:  # record why the run stopped, then stop as before
                log_error("run_stopped", "%s: %s" % (type(e).__name__, str(e)[:150]))
                raise
