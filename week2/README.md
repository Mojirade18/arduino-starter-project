# 🔢 Week 2 — 7-Bit Random Number Display

Build a simple binary number display using **7 LEDs and a push button**.

Each time the button is pressed, the Arduino generates a random number from **0 to 127** and displays it in binary using the LEDs.

<img src="photo_2026-02-20_20-10-31.jpg" width="350">

## 🎯 What You'll Learn

* Binary numbers
* Bits and bit representation
* Digital outputs
* Push buttons
* Random number generation
* Controlling multiple LEDs
* Using the Serial Monitor

## 🧰 Components

* Arduino Uno
* 7 LEDs
* 7 resistors
* Push button
* Breadboard
* Jumper wires

## ⚙️ How It Works

```text
        Push Button
             ↓
      Arduino generates
       random number
             ↓
       Number: 0–127
             ↓
       Convert to binary
             ↓
       ┌─────────────┐
       │ 7 LEDs      │
       │ 1 LED = bit │
       └─────────────┘
```

For example:

```text
Decimal: 5

Binary: 0000101

LEDs:   OFF OFF OFF OFF ON OFF ON
```

The decimal number and LED states are also displayed in the **Serial Monitor**.

## 🚀 How to Run

1. Open `code.ino` in the Arduino IDE.
2. Connect the LEDs and push button.
3. Upload the code.
4. Open the Serial Monitor.
5. Press the button.
6. Observe the LEDs displaying the generated number in binary.

## 🧪 Experiment

Try changing the project.

### Challenge

Can you modify the project so that:

* The LEDs display numbers from **0–127** correctly?
* A second button resets the display?
* The Serial Monitor also shows the binary number?

## 📂 Files

| File                            | Description              |
| ------------------------------- | ------------------------ |
| `code.ino`                      | Arduino source code      |
| `photo_2026-02-20_20-10-31.jpg` | Project image            |
| `photo_2026-02-20_20-10-40.jpg` | Additional project image |
| `photo_2026-02-20_20-10-48.jpg` | Additional project image |
| `smart_light (2).dsn`           | Proteus circuit file     |

---

### 🔢 Learn → Build → Experiment
