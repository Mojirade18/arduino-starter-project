import sys
import re
import subprocess
import tempfile
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:1.5b"
BOARD = "arduino:avr:uno"
MAX_TRIES = 3

TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means.
Use the lab notes below. They are correct, so trust them over your own memory.
Always:
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


def extract_code(reply):
    """Find the code blocks in the AI's reply and return the longest one (the full sketch)."""
    blocks = re.findall(r"```[a-zA-Z+]*\s*\n(.*?)```", reply, re.DOTALL)
    return max(blocks, key=len) if blocks else None


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
        print(f"🤔 Buddy is thinking (attempt {attempt} of {MAX_TRIES})...")
        reply = ask_ai(
            "This Arduino sketch does not compile.\n\n"
            "SKETCH:\n```cpp\n" + code + "\n```\n\n"
            "COMPILER ERRORS:\n" + errors + "\n\n"
            + feedback +
            "1. Explain each error in simple words for a beginner.\n"
            "2. Then give the COMPLETE fixed sketch in one ```cpp code block.\n"
            "Only fix the errors. Do not change anything else."
        )

        fixed = extract_code(reply)
        if fixed is None:
            feedback = "Your last answer had no code block. Remember to include the full fixed sketch.\n\n"
            continue

        print("🔧 Checking Buddy's fix with the compiler...")
        ok, new_errors = compile_code(fixed)
        if ok:
            print("\n" + reply)
            print("\n✅ Verified: Buddy compiled this fix, and it works.")
            return

        feedback = ("Your last fix did NOT compile. It gave these errors:\n"
                    + new_errors + "\nTry again.\n\n")

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
    print(ask_ai(" ".join(sys.argv[1:])))