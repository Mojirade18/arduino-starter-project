"""Arduino Buddy in the browser: a small web server around the same Buddy code."""
import re
import threading
import uuid
from pathlib import Path
from flask import Flask, jsonify, request

from ai import ask_ai, stream_ai, wake_ollama
from compiler import compile_code, only_error_lines
from changes import get_changes, describe
from lab import find_page, PAGES
from buddy import find_fix, build_text, MAX_MEMORY

HERE = Path(__file__).parent
EXAMPLES = HERE / "examples"
app = Flask(__name__)
jobs = {}   # running and finished jobs, by id

HINT_PROMPT = ("A beginner is trying to fix their Arduino sketch by themselves. For EACH change "
               "below, write ONE short hint question that helps them find the problem, like a "
               "teacher would. Do NOT give the answer or write the corrected code.")
WHY_PROMPT = ("A beginner's Arduino sketch was fixed with the changes below. For EACH change, "
              "write one or two simple sentences: what was wrong, and why the change fixes it. "
              "Only talk about these changes. Do not write any code.")


# ---------- The sketch jobs Buddy can do ----------

def task_explain(code, job):
    job["stage"] = "read"
    answer = ask_ai("Explain this Arduino sketch step by step for a beginner. "
                    "Say which pins it uses and what each part does.\n\n" + code)
    return {"answer": answer}


def where_to_look(changes):
    line_numbers = sorted({str(c["line"]) for c in changes if c["line"]}, key=int)
    where = " and ".join(line_numbers) if line_numbers else "the start of the sketch"
    count = "is 1 thing" if len(changes) == 1 else f"are {len(changes)} things"
    return f"There {count} to fix. Look closely at line(s) {where}."


def task_check(code, job):
    """Compile, find a verified fix, and prepare hints + explanation (used by Teach me AND Fix)."""
    job["stage"] = "compile"
    ok, errors = compile_code(code)
    if ok:
        return {"ok": True}
    result = {"ok": False, "errors": only_error_lines(errors), "fixed": None}

    fixed = find_fix(code, errors, report=lambda stage, attempt: job.update(stage=stage, attempt=attempt))
    if fixed is None:
        return result

    job["stage"] = "explain"
    changes = get_changes(code, fixed)
    result.update({
        "fixed": fixed.strip(),
        "changes": [describe(c) for c in changes],
        "changes_data": changes,
        "where": where_to_look(changes) if changes else "Only comments or spacing changed.",
        "hints": build_text(changes, 0, HINT_PROMPT) if changes else "",
        "explanation": build_text(changes, 1, WHY_PROMPT) if changes else "",
    })
    return result


TASKS = {"explain": task_explain, "check": task_check}


# ---------- Web addresses (routes) ----------

@app.get("/")
def home():
    return (HERE / "index.html").read_text()


@app.post("/api/chat")
def start_chat():
    """Start a chat reply. The page then checks back to get the words as they arrive."""
    data = request.get_json(silent=True) or {}
    history = [m for m in data.get("history", [])
               if isinstance(m, dict) and m.get("role") in ("user", "assistant")
               and isinstance(m.get("content"), str)][-MAX_MEMORY:]
    if not history or history[-1]["role"] != "user":
        return jsonify(error="Please type a message first."), 400

    # Find a lab page for the new message, or keep the one the chat was already using
    page = find_page(history[-1]["content"]) or next(
        (p for p in PAGES if p["name"] == data.get("page")), None)

    job_id = uuid.uuid4().hex
    job = {"done": False, "partial": "", "page": page["name"] if page else None}
    jobs[job_id] = job

    def run():
        try:
            for piece in stream_ai(history, page):
                job["partial"] += piece   # the page shows this growing text
            job["done"] = True
        except Exception as error:
            job.update(done=True, error=str(error))

    threading.Thread(target=run, daemon=True).start()
    return jsonify(job=job_id)


@app.post("/api/<task>")
def start_job(task):
    """Start a sketch job in the background and return its id right away."""
    if task not in TASKS:
        return jsonify(error="Unknown task."), 404
    text = (request.get_json(silent=True) or {}).get("text", "").strip()
    if not text:
        return jsonify(error="Please paste some code first."), 400

    job_id = uuid.uuid4().hex
    job = {"done": False, "stage": "start"}
    jobs[job_id] = job

    def run():
        try:
            job.update(result=TASKS[task](text, job), done=True)
        except Exception as error:
            job.update(done=True, error=str(error))

    threading.Thread(target=run, daemon=True).start()
    return jsonify(job=job_id)


@app.get("/api/job/<job_id>")
def check_job(job_id):
    """The page asks this regularly: is the job done yet, and which step is it on?"""
    return jsonify(jobs.get(job_id, {"done": True, "error": "Unknown job."}))


def example_names():
    return sorted(p.name for p in EXAMPLES.iterdir() if p.is_dir())


@app.get("/api/examples")
def list_examples():
    return jsonify(example_names())


@app.get("/api/examples/<name>")
def get_example(name):
    if name not in example_names():   # only allow real example folders
        return jsonify(error="No such example."), 404
    return jsonify(code=(EXAMPLES / name / f"{name}.ino").read_text())


@app.get("/api/weeks")
def list_weeks():
    """The lab weeks for the sidebar and cards, with the first README heading as the title."""
    weeks = []
    for page in PAGES:
        if page["name"].startswith("week"):
            heading = re.search(r"^#+\s*(.+)$", page["text"], re.MULTILINE)
            weeks.append({"name": page["name"],
                          "title": heading.group(1).strip() if heading else page["name"]})
    return jsonify(weeks)


if __name__ == "__main__":
    wake_ollama()
    print("🌐 Arduino Buddy web is running! Open port 8000 in your browser.")
    app.run(host="0.0.0.0", port=8000)