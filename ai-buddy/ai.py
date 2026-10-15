"""Everything about talking to the AI model (Qwen, through Ollama)."""
import subprocess
import time
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:1.5b"
KEEP_ALIVE = "30m"                # keep the model loaded for 30 minutes, so the next answer starts faster
OPTIONS = {"num_predict": 1024}   # limit answer length: faster, and stops rambling

TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means.
Use the lab notes below. They are correct, so trust them over your own memory.
If a question is unclear or missing details, ask the student what they mean instead of guessing."""

NOTES = (Path(__file__).parent / "lab_notes.md").read_text()


def system_message(page=None):
    """The rules + lab notes, plus a lab page if one was found."""
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
        keep_alive=KEEP_ALIVE,
        options=OPTIONS,
    )
    return response["message"]["content"]


def stream_ai(history, page=None):
    """Send a whole conversation to Qwen and give back the answer piece by piece."""
    stream = ollama.chat(
        model=MODEL,
        messages=[system_message(page)] + history,
        stream=True,
        keep_alive=KEEP_ALIVE,
        options=OPTIONS,
    )
    for chunk in stream:
        yield chunk["message"]["content"]


def chat_ai(history, page=None):
    """Terminal chat: print the answer word by word, and return it."""
    reply = ""
    for piece in stream_ai(history, page):
        print(piece, end="", flush=True)
        reply += piece
    print()
    return reply


def ollama_is_running():
    """Check whether the Ollama engine is answering."""
    try:
        ollama.list()
        return True
    except Exception:
        return False


def wake_ollama():
    """Start Ollama in the background if it's asleep. Returns True when it's ready."""
    if ollama_is_running():
        return True
    print("😴 Ollama was asleep. Waking it up...")
    log = open(Path(__file__).parent / "ollama.log", "a")
    try:
        subprocess.Popen(["ollama", "serve"], stdout=log, stderr=log, start_new_session=True)
    except FileNotFoundError:
        print("⚠️ Ollama isn't installed. See the Setup section in README.md.")
        return False
    for _ in range(20):            # wait up to 10 seconds
        time.sleep(0.5)
        if ollama_is_running():
            print("☀️ Ollama is awake!\n")
            return True
    print("⚠️ Couldn't start Ollama. Try:  ollama serve > ollama.log 2>&1 &")
    return False