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


# ---------- Talking to the AI ----------

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


# ---------- Compiling ----------

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


# ---------- Comparing code ----------

def extract_code(reply):
    """Find the code blocks in the AI's reply and return the longest one (the full sketch)."""
    blocks = re.findall(r"```[a-zA-Z+]*\s*\n(.*?)```", reply, re.DOTALL)
    return max(blocks, key=len) if blocks else None


def strip_comment(line):
    """Remove // comments and extra spaces, so we only compare real code."""
    return line.split("//")[0].strip()


def get_changes(original, fixed):
    """Compare the original and fixed sketches. Returns a list of changes."""
    old = [(n, strip_comment(l)) for n, l in enumerate(original.splitlines(), 1) if strip_comment(l)]
    new = [strip_comment(l) for l in fixed.splitlines() if strip_comment(l)]
    old_text = [text for _, text in old]

    changes = []
    matcher = difflib.SequenceMatcher(None, old_text, new)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                changes.append({
                    "kind": "replace",
                    "line": old[min(i1 + k, i2 - 1)][0],
                    "before": old_text[i1 + k] if i1 + k < i2 else "",
                    "after": new[j1 + k] if j1 + k < j2 else "",
                })
        elif tag == "delete":
            for k in range(i1, i2):
                changes.append({"kind": "delete", "line": old[k][0],
                                "before": old_text[k], "after": ""})
        elif tag == "insert":
            for k in range(j1, j2):
                changes.append({"kind": "insert", "line": old[i1 - 1][0] if i1 > 0 else 0,
                                "before": "", "after": new[k]})
    return changes


def describe(change):
    """Turn one change into a readable line of text."""
    n, before, after = change["line"], change["before"], change["after"]
    if change["kind"] == "delete":
        return f"Line {n}:  remove   {before}"
    if change["kind"] == "insert":
        return f"After line {n}:  add   {after}" if n else f"At the start:  add   {after}"
    return f"Line {n}:  {before}   →   {after}"


# ---------- Rules for common beginner mistakes (no AI needed) ----------

def inserted_text(before, after):
    """If 'after' is just 'before' with some characters added, return those characters."""
    added = ""
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, before, after).get_opcodes():
        if tag == "insert":
            added += after[j1:j2]
        elif tag != "equal":
            return None
    return added


def rule_for(change):
    """Recognize a common mistake. Returns (hint, explanation), or None if no rule matches."""
    n, before, after = change["line"], change["before"], change["after"]

    # Missing closing brace }
    if change["kind"] == "insert" and after == "}":
        return (f"Around line {n}, a block of code is never closed. "
                "Every { needs a matching }. Try counting them!",
                f"A closing brace }} was missing after line {n}. Every {{ that starts a block "
                "(like setup or loop) needs a } to end it.")

    if change["kind"] != "replace":
        return None

    # Missing semicolon, or missing brackets
    added = inserted_text(before, after)
    if added == ";":
        return (f"Something small is missing at the end of line {n}. "
                "What do most Arduino lines end with?",
                f"Line {n} was missing a semicolon (;) at the end. Every Arduino instruction "
                "must end with ; so the compiler knows where it stops. The compiler often "
                "reports this error on the NEXT line, because that's where it notices.")
    if added and set(added) <= set(";)]}"):
        return (f"Line {n} isn't finished. Count the brackets: "
                "does every ( have a matching ) ?",
                f"Line {n} was missing  {added}  . Every opening bracket needs "
                "a closing one, and every instruction must end with ;")

    # A misspelled name, or wrong capital letters
    old_words = re.findall(r"[A-Za-z_]\w*", before)
    new_words = re.findall(r"[A-Za-z_]\w*", after)
    if len(old_words) == len(new_words):
        different = [(o, w) for o, w in zip(old_words, new_words) if o != w]
        if len(different) == 1:
            wrong, right = different[0]
            if before.replace(wrong, right) == after:
                if wrong.lower() == right.lower():
                    return (f"On line {n}, look closely at `{wrong}`. Arduino cares about "
                            "capital letters. Is every letter the right size?",
                            f"Line {n} wrote `{wrong}`, but the correct name is `{right}`. "
                            "Arduino is case-sensitive: capital and small letters count "
                            "as different letters.")
                return (f"On line {n}, the name `{wrong}` doesn't exist. Compare it with "
                        "the names created at the top of your sketch. "
                        "Is it spelled exactly the same?",
                        f"Line {n} used `{wrong}`, but nothing with that name exists. "
                        f"The correct name is `{right}`. The error 'was not declared in "
                        "this scope' usually means a typo like this.")
    return None


def build_text(changes, part, ai_question):
    """Use rules where possible (part 0 = hint, 1 = explanation), and the AI for the rest."""
    lines, unknown = [], []
    for change in changes:
        rule = rule_for(change)
        if rule:
            lines.append("  ✔ " + rule[part])
        else:
            unknown.append(change)
    if unknown:
        print("\n💬 Buddy is asking the AI about the unusual part...")
        answer = ask_ai(ai_question + "\n\nChanges:\n" + "\n".join(describe(c) for c in unknown))
        lines.append("  🤖 (from the AI, may be less accurate)\n" + answer)
    return "\n".join(lines)


# ---------- Finding a verified fix (used by debug AND hint) ----------

def find_fix(code, errors):
    """Ask the AI for a fix and check it with the compiler. Returns the fixed code, or None."""
    feedback = ""
    for attempt in range(1, MAX_TRIES + 1):
        print(f"   ...attempt {attempt} of {MAX_TRIES}")
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
        ok, new_errors = compile_code(fixed)
        if ok:
            return fixed
        feedback = ("Your last fix did NOT compile. It gave these errors:\n"
                    + only_error_lines(new_errors) + "\nTry again.\n\n")
    return None


def show_answer(fixed, changes):
    """Print the verified fix, the exact changes, and the explanation."""
    print("\n✅ Verified fix (Buddy compiled it, and it works):\n")
    print(fixed.strip())
    print("\n📝 What Buddy changed (found by comparing the files, not by the AI):")
    if not changes:
        print("  Only comments or spacing changed.")
        return
    for change in changes:
        print("  " + describe(change))
    print("\n💬 Why these changes fix it:")
    print(build_text(changes, 1,
        "A beginner's Arduino sketch was fixed with the changes below. For EACH change, "
        "write one or two simple sentences: what was wrong, and why the change fixes it. "
        "Only talk about these changes. Do not write any code."))
    print("\n   ✔ = from Buddy's rules (always matches the fix) · 🤖 = from the AI")


# ---------- Commands ----------

def debug(path):
    code = Path(path).read_text()

    print("🔧 Compiling your sketch...")
    ok, errors = compile_code(code)
    if ok:
        print("✅ Your sketch compiles with no errors!")
        return

    print("❌ The compiler found errors:\n")
    print(errors)

    print("🤔 Buddy is fixing the code...")
    fixed = find_fix(code, errors)
    if fixed is None:
        print(f"\n⚠️ Buddy couldn't find a fix that compiles after {MAX_TRIES} tries. "
              "Look at the errors above, or ask a friend or mentor.")
        return

    show_answer(fixed, get_changes(code, fixed))


def next_step():
    """Wait for the user. Returns True if they want to jump to the answer."""
    choice = input("\n   [Enter] next hint · type 'answer' to see the fix · [Ctrl+C] go try it yourself: ")
    return choice.strip().lower() == "answer"


def hint(path):
    code = Path(path).read_text()

    print("🔧 Compiling your sketch...")
    ok, errors = compile_code(code)
    if ok:
        print("✅ Your sketch compiles with no errors! No hints needed.")
        return

    error_lines = only_error_lines(errors)
    print(f"❌ The compiler found {len(error_lines.splitlines())} error(s):\n")
    print(error_lines)

    print("\n🤔 Buddy is preparing hints (this can take a few minutes)...")
    fixed = find_fix(code, errors)
    if fixed is None:
        print("\n⚠️ Buddy couldn't find a verified fix, so it won't guess. "
              "Try the error messages above, or ask a friend or mentor.")
        return

    changes = get_changes(code, fixed)
    if not changes:
        print("\nBuddy's fix only changed comments or spacing. Try running the compiler again.")
        return

    # Hint 1: where to look (no AI)
    line_numbers = sorted({str(c["line"]) for c in changes if c["line"]}, key=int)
    where = " and ".join(line_numbers) if line_numbers else "the start of the sketch"
    count = "is 1 thing" if len(changes) == 1 else f"are {len(changes)} things"
    print(f"\n💡 Hint 1: There {count} to fix. Look closely at line(s) {where}.")
    if next_step():
        show_answer(fixed, changes)
        return

    # Hint 2: a guiding hint for each change (rules first, AI only if needed)
    print("\n💡 Hint 2:")
    print(build_text(changes, 0,
        "A beginner is trying to fix their Arduino sketch by themselves. For EACH change "
        "below, write ONE short hint question that helps them find the problem, like a "
        "teacher would. Do NOT give the answer or write the corrected code."))
    if next_step():
        show_answer(fixed, changes)
        return

    # Hint 3: the exact changes (no AI)
    print("\n💡 Hint 3: Here is exactly what needs to change:")
    for change in changes:
        print("  " + describe(change))
    input("\n   Try making these changes yourself! Press [Enter] to see the full fix and explanation...")

    show_answer(fixed, changes)


# ----- Choose what to do based on the first word typed -----
if len(sys.argv) >= 3 and sys.argv[1] == "explain":
    sketch = Path(sys.argv[2]).read_text()
    print(ask_ai("Explain this Arduino sketch step by step for a beginner. "
                 "Say which pins it uses and what each part does.\n\n" + sketch))
elif len(sys.argv) >= 3 and sys.argv[1] == "debug":
    debug(sys.argv[2])
elif len(sys.argv) >= 3 and sys.argv[1] == "hint":
    hint(sys.argv[2])
else:
    print(ask_ai(" ".join(sys.argv[1:]) + "\n\n" + QUESTION_STYLE))