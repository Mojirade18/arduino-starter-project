"""Rules that recognize common beginner mistakes, without using the AI."""
import re
import difflib


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