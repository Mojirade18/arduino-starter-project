# 💧 Week 3 — Water Leak Detector

Build a simple system that detects the presence of water using a **water sensor** and Arduino.

When water is detected, the LED turns on and the system displays **"Water Detected!"** in the Serial Monitor.

<img src="photo_2026-03-17_22-25-05.jpg" width="350">

## 🎯 What You'll Learn

* How water sensors work
* Digital input
* Reading sensor states
* Using `digitalRead()`
* Detecting changes in sensor state
* Controlling an LED
* Serial Monitor debugging

## 🧰 Components

* Arduino Uno
* Water sensor
* LED
* Resistor
* Breadboard
* Jumper wires

## ⚙️ How It Works

```text
       Water Sensor
             ↓
       Arduino reads
        sensor state
             ↓
       ┌─────────────┐
       │             │
     Water         Dry
       │             │
       ↓             ↓
    LED ON        LED OFF
       │             │
       └──────┬──────┘
              ↓
        Serial Monitor
```

When the sensor detects water, the Arduino responds by turning on the LED and displaying a message.

The system also detects when the surface changes back to dry.

## 🚀 How to Run

1. Open `code.ino` in the Arduino IDE.
2. Connect the water sensor and LED.
3. Upload the code.
4. Open the Serial Monitor.
5. Place water on the sensor.
6. Observe the LED and Serial Monitor.

### 🧪 Simulation

The repository also contains `code_simulation.ino`.

This version uses a **switch instead of the physical water sensor**, making it possible to test the project in Proteus.

## 🧪 Experiment

Try modifying the project.

### Challenge

Can you make the system:

* Turn on a buzzer when water is detected?
* Display a different message when the surface becomes dry?
* Keep track of how many times water was detected?

## 📂 Files

| File                            | Description                |
| ------------------------------- | -------------------------- |
| `code.ino`                      | Arduino source code        |
| `code_simulation.ino`           | Simulation/testing version |
| `photo_2026-03-17_22-25-05.jpg` | Project image              |
| `photo_2026-03-17_22-25-32.jpg` | Additional project image   |

---

### 💧 Learn → Build → Experiment
