"""Everything about talking to the AI model (Qwen, through Ollama)."""
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:1.5b"

TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means.
Use the lab notes below. They are correct, so trust them over your own memory."""

NOTES = (Path(__file__).parent / "lab_notes.md").read_text()


def ask_ai(question):
    """Send a question to Qwen (with teacher rules + lab notes) and return the answer."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": TEACHER + "\n\n" + NOTES},
            {"role": "user", "content": question},
        ],
    )
    return response["message"]["content"]