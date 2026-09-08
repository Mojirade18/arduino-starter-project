# 👏 Week 4 — Sound-Activated LED

Build a simple **clap switch** using a sound sensor and Arduino.

When the sensor detects a clap or loud sound, the LED turns **ON for 2 seconds** and then turns off.

<img src="photo_2026-03-29_21-16-15.jpg" width="350">

## 🎯 What You'll Learn

* How sound sensors work
* Digital input
* Detecting sound events
* Timing in Arduino
* Controlling an LED
* Using conditions in Arduino

## 🧰 Components

* Arduino Uno
* Sound sensor module
* LED
* Resistor
* Breadboard
* Jumper wires

## ⚙️ How It Works

```text
       Sound / Clap
             ↓
       Sound Sensor
             ↓
          Arduino
             ↓
        Sound detected?
          ↙       ↘
        YES        NO
         ↓          ↓
      LED ON      LED OFF
         ↓
      2 seconds
         ↓
      LED OFF
```

The Arduino continuously monitors the sound sensor.

When a sound is detected, the LED turns on for **2 seconds** before switching off.

## 🚀 How to Run

1. Open `code.ino` in the Arduino IDE.
2. Connect the sound sensor and LED.
3. Upload the code.
4. Make a clap or loud sound near the sensor.
5. Observe the LED.

## 🧪 Experiment

Try modifying the project.

### Challenge

Can you:

* Make the LED stay on for longer?
* Use a second LED?
* Add a buzzer?
* Make each clap toggle the LED **ON/OFF** instead of using a fixed 2-second timer?

## 📂 Files

| File                                | Description         |
| ----------------------------------- | ------------------- |
| `code.ino`                          | Arduino source code |
| `photo_2026-03-17_22-25-05 (1).jpg` | Project image       |
| `photo_2026-03-29_21-16-15.jpg`     | Project image       |

---

### 👏 Learn → Build → Experiment
