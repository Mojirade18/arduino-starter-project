"""Finding the right lab page for each question (a simple version of RAG)."""
import re
from pathlib import Path

REPO = Path(__file__).parent.parent      # the main arduino-starter-project folder
README_CHARS = 2000                      # keep pages short enough for the AI to read
CODE_CHARS = 2000

# Common words that don't help find the right page
SKIP = {"the", "and", "for", "you", "what", "how", "why", "does", "this", "that",
        "with", "can", "are", "use", "using", "when", "will", "your", "have", "not",
        "get", "would", "should", "arduino", "code", "sketch"}


def main_sketch(folder):
    """Find the main .ino file in a folder (prefer code.ino, skip simulation versions)."""
    if (folder / "code.ino").exists():
        return folder / "code.ino"
    sketches = [f for f in sorted(folder.glob("*.ino")) if "simulation" not in f.name]
    return sketches[0] if sketches else None


def load_pages():
    """Read every week's README and main sketch, plus the beginner challenges."""
    pages = []
    folders = sorted(REPO.glob("week*")) + [REPO / "beginner-challenges"]
    for folder in folders:
        readme = folder / "README.md"
        if not readme.exists():
            continue
        text = "README:\n" + readme.read_text()[:README_CHARS]
        sketch = main_sketch(folder)
        if sketch:
            text += f"\n\nTHE CODE ({sketch.name}). Pin numbers here are always correct:\n"
            text += sketch.read_text()[:CODE_CHARS]
        pages.append({"name": folder.name, "text": text})
    return pages


PAGES = load_pages()


def words(text):
    """Turn text into a set of useful lowercase words."""
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2 and w not in SKIP}


def find_page(question):
    """Return the page that best matches the question, or None if nothing matches well."""
    question_words = words(question)
    asked = question.lower().replace(" ", "")   # so "week 3" also matches "week3"
    best, best_score = None, 0
    for page in PAGES:
        score = len(question_words & words(page["text"]))
        if page["name"] in asked:
            score += 10   # they named the folder directly, e.g. "week3"
        if score > best_score:
            best, best_score = page, score
    return best if best_score >= 2 else None