"""Arduino Buddy: a free, offline AI teacher for Arduino beginners."""
import sys
from pathlib import Path

from ai import ask_ai
from compiler import compile_code, only_error_lines
from changes import extract_code, get_changes, describe
from rules import rule_for

MAX_TRIES = 3

# Extra rules used only for normal questions
QUESTION_STYLE = """Answer rules:
- Give exact names, not vague words like "something else".
- Include a short Arduino code example.
- End with one tip that helps a beginner avoid a common mistake."""


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
if __name__ == "__main__":
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