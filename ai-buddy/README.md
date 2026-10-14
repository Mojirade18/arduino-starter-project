# 🤖 Arduino Buddy

**A free, offline AI teacher for Arduino beginners. It knows the lab, gives hints before answers, and only shows fixes that actually compile.**

Arduino Buddy runs a small open-weight AI model on your own computer. No paid AI service, no account, and your code never leaves your machine.

```
You:    python buddy.py hint examples/broken_case/broken_case.ino

Buddy:  ❌ The compiler found 2 error(s)
        💡 Hint 1: There are 2 things to fix. Look closely at line(s) 6 and 9.
        💡 Hint 2:
          ✔ On line 6, look closely at `digitalwrite`. Arduino cares about
            capital letters. Is every letter the right size?
          ✔ Line 9 isn't finished. Count the brackets: does every ( have a matching ) ?
        💡 Hint 3: Here is exactly what needs to change...
        ✅ Verified fix (Buddy compiled it, and it works)
```

---

## ✨ What makes Buddy different

| | Arduino IDE | ChatGPT | **Arduino Buddy** |
|---|---|---|---|
| Finds the real compiler error | ✅ | ❌ guesses | ✅ |
| Explains it in simple words | ❌ | ✅ | ✅ |
| Suggests a fix | ❌ | ✅ | ✅ |
| **Checks the fix actually compiles** | ❌ | ❌ | ✅ |
| Gives hints instead of the answer | ❌ | ❌ | ✅ |
| Knows this lab's projects and pins | ❌ | ❌ | ✅ |
| Free, private, works offline | ✅ | ❌ | ✅ |

---

## 🧰 Commands

| Command | What it does |
|---|---|
| `python buddy.py "your question"` | Answers an Arduino question, using the lab pages when relevant |
| `python buddy.py chat` | A conversation where Buddy remembers what you said |
| `python buddy.py explain path/to/sketch.ino` | Explains a sketch step by step |
| `python buddy.py debug path/to/sketch.ino` | Compiles the sketch, fixes errors, and **verifies the fix compiles** |
| `python buddy.py hint path/to/sketch.ino` | Like `debug`, but teaches with 3 hints before showing the fix |

Try `debug` and `hint` on the broken examples in [`examples/`](examples/).

---

## 🚀 Setup

Works on Linux, macOS, and GitHub Codespaces. You need **Python 3.9+** and about **2 GB** of free disk space.

**1. Install Ollama** (the program that runs the AI model):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

On Windows or macOS, you can also download it from [ollama.com](https://ollama.com/download).

**2. Start Ollama and download the model** (about 1 GB, only once):

```bash
ollama serve > ollama.log 2>&1 &
ollama pull qwen2.5-coder:1.5b
```

**3. Install the Arduino compiler** (`arduino-cli`, the same compiler used inside the Arduino IDE):

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=$HOME/.local/bin sh
arduino-cli core update-index
arduino-cli core install arduino:avr
```

**4. Install the Python library:**

```bash
cd ai-buddy
pip install -r requirements.txt
```

**5. Try it!**

```bash
python buddy.py hint examples/broken_blink/broken_blink.ino
```

> 💡 **In Codespaces:** Ollama stops when your Codespace goes to sleep. Each time you come back, run `ollama serve > ollama.log 2>&1 &` before using Buddy.

---

## 🔍 How it works

```
                 your sketch
                      │
                      ▼
          ┌───────────────────────┐
          │  arduino-cli compile   │ ── no errors ──▶ ✅ "Your sketch compiles!"
          └───────────────────────┘
                      │ errors
                      ▼
          ┌───────────────────────┐
          │  AI writes a fix       │ ◀───────────────┐
          └───────────────────────┘                  │
                      │                              │ didn't compile:
                      ▼                              │ tell the AI why,
          ┌───────────────────────┐                  │ try again (max 3)
          │  arduino-cli compile   │ ─────────────────┘
          │  the AI's fix          │
          └───────────────────────┘
                      │ compiles
                      ▼
   📝 Compare files → exact changes (no AI, always correct)
   ✔  Rules recognize common mistakes → hints & explanations
   🤖 AI explains only what the rules don't recognize
```

**The main idea:** a small AI is helpful but makes mistakes, so Buddy only trusts it where it can check the result.

| Part of the answer | Comes from | Trust |
|---|---|---|
| ❌ Compiler errors | arduino-cli | Always correct |
| ✅ Verified fix | AI, checked by the compiler | Always compiles |
| 📝 What changed | Comparing the files | Always correct |
| ✔ Hints and explanations | Buddy's rules (`rules.py`) | Always match the fix |
| 🤖 Other explanations | AI only | May be less accurate |

### Knowing the lab (RAG)

When you ask a question, Buddy searches each week's `README.md` and `code.ino` for matching words and sends the best match to the AI along with your question. It shows which page it used:

```
You: which pin is the water leak sensor on?
   📚 Using the lab page: week3 (README + code)
Buddy: The water leak sensor is connected to pin 2 on the Arduino Uno.
```

Without the code, the AI once guessed "pin 0", because the README doesn't mention pins. With the code, it answers correctly. **An AI can only be as accurate as the information you give it.**

---

## 📁 Project structure

```
ai-buddy/
├── buddy.py         # the commands (debug, hint, explain, chat, questions)
├── ai.py            # talks to the AI model through Ollama
├── compiler.py      # compiles sketches with arduino-cli
├── changes.py       # compares the original and fixed sketches
├── rules.py         # ✔ rules for common beginner mistakes
├── lab.py           # finds the right lab page for each question
├── lab_notes.md     # correct Arduino facts the AI must follow
├── requirements.txt
└── examples/        # broken sketches to practice with
```

---

## ⚠️ Honest limitations

- **It's slow.** The model runs on your CPU, so answers can take 1–3 minutes. Free and private comes at a cost.
- **The small model makes mistakes.** That's why Buddy verifies fixes and labels AI-only text with 🤖. Always read 🤖 explanations carefully.
- **Arduino Uno only** for now (`BOARD` in `compiler.py`).
- **Compile errors only.** Buddy can't see wiring problems or check what your circuit actually does, yet.

---

## 🤝 Contributing

Ideas for first contributions:

- **Add a rule** to `rules.py` for another common beginner mistake (for example, `=` instead of `==` in an `if`).
- **Add a broken example** to `examples/` with a mistake Buddy doesn't handle well yet.
- **Add facts** to `lab_notes.md`.
- **Support more boards** (Nano, Mega).

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) to get started.

---

## 🌍 Why open-weight AI?

Paid AI tools aren't affordable for every student, and they need a constant internet connection. Arduino Buddy uses **Qwen2.5-Coder 1.5B**, an open-weight model anyone can download and run for free on an ordinary computer. Your code stays on your machine, and anyone can study, change, or improve how Buddy works.

**AI belongs to everyone, including beginners learning hardware.**