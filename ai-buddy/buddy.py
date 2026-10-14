import sys
import re
import subprocess
import tempfile
import difflib
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:1.5b"
BOARD = "arduino:avr:uno"
MAX_TRIES = 3

TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means.
Use the lab notes below. They are correct, so trust them over your own memory."""

# Extra rules used only for normal questions
QUESTION_STYLE = """Answer rules:
- Give exact names, not vague words like "something else".
- Include a short Arduino code example.
- End with one tip that helps a beginner avoid a common mistake."""

notes = (Path(__file__).parent / "lab_notes.md").read_text()


def ask_ai(question):
    """Send a question to Qwen (with teacher rules + lab notes) and return the answer."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": TEACHER + "\n\n" + notes},
            {"role": "user", "content": question},
        ],
    )
    return response["message"]["content"]


def compile_code(code):
    """Compile Arduino code with arduino-cli. Returns (worked?, error messages)."""
    with tempfile.TemporaryDirectory() as tmp:
        sketch_dir = Path(tmp) / "sketch"
        sketch_dir.mkdir()
        sketch_file = sketch_dir / "sketch.ino"
        sketch_file.write_text(code)
        result = subprocess.run(
            ["arduino-cli", "compile", "--fqbn", BOARD, str(sketch_dir)],
            capture_output=True, text=True,
        )
        output = (result.stdout + result.stderr).replace(str(sketch_file), "sketch.ino")
        return result.returncode == 0, output


def only_error_lines(errors):
    """Keep just the lines that say 'error:', so the AI isn't distracted by the rest."""
    return "\n".join(line for line in errors.splitlines() if "error:" in line)


def extract_code(reply):
    """Find the code blocks in the AI's reply and return the longest one (the full sketch)."""
    blocks = re.findall(r"```[a-zA-Z+]*\s*\n(.*?)```", reply, re.DOTALL)
    return max(blocks, key=len) if blocks else None


def strip_comment(line):
    """Remove // comments and extra spaces, so we only compare real code."""
    return line.split("//")[0].strip()


def get_changes(original, fixed):
    """Compare the original and fixed sketches. Returns a list of changes as text."""
    old = [(n, strip_comment(l)) for n, l in enumerate(original.splitlines(), 1) if strip_comment(l)]
    new = [strip_comment(l) for l in fixed.splitlines() if strip_comment(l)]
    old_text = [text for _, text in old]

    changes = []
    matcher = difflib.SequenceMatcher(None, old_text, new)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                line_no = old[min(i1 + k, i2 - 1)][0]
                before = old_text[i1 + k] if i1 + k < i2 else "(nothing)"
                after = new[j1 + k] if j1 + k < j2 else "(removed)"
                changes.append(f"Line {line_no}:  {before}   →   {after}")
        elif tag == "delete":
            for k in range(i1, i2):
                changes.append(f"Line {old[k][0]}:  removed   {old_text[k]}")
        elif tag == "insert":
            for k in range(j1, j2):
                changes.append(f"Added:  {new[k]}")
    return changes


def debug(path):
    code = Path(path).read_text()

    print("🔧 Compiling your sketch...")
    ok, errors = compile_code(code)
    if ok:
        print("✅ Your sketch compiles with no errors!")
        return

    print("❌ The compiler found errors:\n")
    print(errors)

    feedback = ""
    for attempt in range(1, MAX_TRIES + 1):
        # Job 1: ask the AI ONLY for the fixed code
        print(f"🤔 Buddy is fixing the code (attempt {attempt} of {MAX_TRIES})...")
        reply = ask_ai(
            "This Arduino sketch does not compile.\n\n"
            "SKETCH:\n```cpp\n" + code + "\n```\n\n"
            "COMPILER ERRORS:\n" + only_error_lines(errors) + "\n\n"
            + feedback +
            "Reply with ONLY the complete fixed sketch in one ```cpp code block.\n"
            "Only fix the errors. Do not change anything else. "
            "Do not add comments. Do not write any explanation."
        )

        fixed = extract_code(reply)
        if fixed is None:
            feedback = "Your last answer had no code block. Reply with the full fixed sketch in a ```cpp block.\n\n"
            continue

        # Check the fix with the real compiler
        print("🔧 Checking Buddy's fix with the compiler...")
        ok, new_errors = compile_code(fixed)
        if not ok:
            feedback = ("Your last fix did NOT compile. It gave these errors:\n"
                        + only_error_lines(new_errors) + "\nTry again.\n\n")
            continue

        # The fix works! Show it.
        print("\n✅ Verified fix (Buddy compiled it, and it works):\n")
        print(fixed.strip())

        changes = get_changes(code, fixed)
        print("\n📝 What Buddy changed (found by comparing the files, not by the AI):")
        if not changes:
            print("  Only comments or spacing changed.")
            return
        for change in changes:
            print("  " + change)

        # Job 2: ask the AI to explain ONLY the real, verified changes
        print("\n💬 Buddy is explaining the changes...")
        explanation = ask_ai(
            "A beginner's Arduino sketch had these compiler errors:\n"
            + only_error_lines(errors) + "\n\n"
            "These exact changes fixed it:\n" + "\n".join(changes) + "\n\n"
            "For EACH change, write one or two simple sentences: "
            "what was wrong, and why the change fixes it.\n"
            "Only talk about these changes. Do not mention anything else. "
            "Do not write any code."
        )
        print("\n" + explanation)
        return

    print("\n⚠️ Buddy couldn't find a fix that compiles after "
          f"{MAX_TRIES} tries. Look at the errors above, or ask a friend or mentor.")


# ----- Choose what to do based on the first word typed -----
if len(sys.argv) >= 3 and sys.argv[1] == "explain":
    sketch = Path(sys.argv[2]).read_text()
    print(ask_ai("Explain this Arduino sketch step by step for a beginner. "
                 "Say which pins it uses and what each part does.\n\n" + sketch))
elif len(sys.argv) >= 3 and sys.argv[1] == "debug":
    debug(sys.argv[2])
else:
    print(ask_ai(" ".join(sys.argv[1:]) + "\n\n" + QUESTION_STYLE))