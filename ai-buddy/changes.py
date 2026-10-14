"""Comparing the original sketch with the fixed one."""
import re
import difflib


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