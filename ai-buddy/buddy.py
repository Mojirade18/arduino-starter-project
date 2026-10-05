import sys
import ollama

# Which AI model to use (the one you downloaded)
MODEL = "qwen2.5-coder:1.5b"

# The instructions that turn Qwen into Arduino Buddy
TEACHER = """You are Arduino Buddy, a patient teacher for complete beginners.
Explain things in simple words and short sentences.
If you must use a technical word, explain what it means."""

# Join everything the user typed after "python buddy.py" into one question
question = " ".join(sys.argv[1:])

# Send the instructions + question to Qwen through Ollama
response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": TEACHER},
        {"role": "user", "content": question},
    ],
)

# Print the answer
print(response["message"]["content"])