"""Everything about talking to the AI model (Qwen, through Ollama)."""
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:1.5b"

TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means.
Use the lab notes below. They are correct, so trust them over your own memory.
If a question is unclear or missing details, ask the student what they mean instead of guessing."""

NOTES = (Path(__file__).parent / "lab_notes.md").read_text()


def system_message(page=None):
    """The rules + lab notes, plus a lab README page if one was found."""
    content = TEACHER + "\n\n" + NOTES
    if page:
        content += ("\n\nRELEVANT PAGE FROM THE LAB (" + page["name"] + "). "
                    "Use it when it helps answer the question:\n" + page["text"])
    return {"role": "system", "content": content}


def ask_ai(question, page=None):
    """Send one question to Qwen and return the full answer."""
    response = ollama.chat(
        model=MODEL,
        messages=[system_message(page), {"role": "user", "content": question}],
    )
    return response["message"]["content"]


def chat_ai(history, page=None):
    """Send a whole conversation to Qwen, print the answer word by word, and return it."""
    stream = ollama.chat(model=MODEL, messages=[system_message(page)] + history, stream=True)
    reply = ""
    for chunk in stream:
        piece = chunk["message"]["content"]
        print(piece, end="", flush=True)   # show each piece as soon as it arrives
        reply += piece
    print()
    return reply