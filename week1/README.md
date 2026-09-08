# 💡 Week 1 — Light-Activated LED

Build a simple automatic light using an **LDR sensor** and an Arduino.

When the environment becomes dark, the LED turns **ON**. When there is enough light, the LED turns **OFF**.

<img src="smart_light.BMP" width="350">

## 🎯 What You'll Learn

* How an LDR works
* Reading analog values with Arduino
* Using `analogRead()`
* Setting threshold values
* Using `if/else` conditions
* Controlling an LED
* Viewing sensor readings in the Serial Monitor

## 🧰 Components

* Arduino Uno
* LDR
* LED
* Resistor
* Breadboard
* Jumper wires

## ⚙️ How It Works

```text
Light Level
     ↓
   LDR
     ↓
 Arduino reads value
     ↓
 Compare with threshold
     ↓
 ┌───────────────┐
 │               │
Dark           Bright
 │               │
 ↓               ↓
LED ON          LED OFF
```

The Arduino continuously reads the LDR value.

If the value indicates that the environment is dark, the LED turns on.

If the environment is bright, the LED turns off.

The sensor reading is also displayed in the **Serial Monitor**.

## 🚀 How to Run

1. Open `code.ino` in the Arduino IDE.
2. Connect your Arduino and components.
3. Upload the code.
4. Open the Serial Monitor.
5. Change the amount of light reaching the LDR.
6. Observe the LED and sensor readings.

## 🧪 Experiment

Try changing the **light threshold** in the code.

### Challenge

Can you modify the project so that:

* The LED turns on only when it is **very dark**?
* The LED turns off when the environment becomes bright?
* You can determine the best threshold using the Serial Monitor?

## 📂 Files

| File                 | Description          |
| -------------------- | -------------------- |
| `code.ino`           | Arduino source code  |
| `smart_light.BMP`    | Project image        |
| `smart_light.dsn`    | Proteus circuit file |
| `smart_light.pdsprj` | Proteus project file |

---

### 💡 Learn → Build → Experiment
