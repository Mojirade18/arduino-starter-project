import sys
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:1.5b"

TEACHER = TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means.
Use the lab notes below. They are correct, so trust them over your own memory.
Always:
- Give exact names, not vague words like "something else".
- Include a short Arduino code example.
- End with one tip that helps a beginner avoid a common mistake."""

# Read the lab notes file that sits next to this script
notes = (Path(__file__).parent / "lab_notes.md").read_text()

question = " ".join(sys.argv[1:])

response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": TEACHER + "\n\n" + notes},
        {"role": "user", "content": question},
    ],
)

print(response["message"]["content"])