# 📏 Week 5 — Ultrasonic Proximity Alarm

Build a proximity alarm using an **HC-SR04 ultrasonic sensor**, LED, and buzzer.

The Arduino measures the distance to an object. When an object comes closer than **20 cm**, the LED turns on and the buzzer produces an alert.

## 🎯 What You'll Learn

* How ultrasonic sensors work
* Measuring distance with the HC-SR04
* Using `digitalWrite()`
* Conditional logic
* Working with buzzers
* Creating sensor-based alerts
* Reading sensor data

## 🧰 Components

* Arduino Uno
* HC-SR04 ultrasonic sensor
* LED
* Buzzer
* Resistor
* Breadboard
* Jumper wires

## ⚙️ How It Works

```text
       HC-SR04
          ↓
    Measure distance
          ↓
    Arduino processes
       the value
          ↓
    Is object < 20 cm?
       ↙          ↘
     YES           NO
      ↓             ↓
  LED + Buzzer     Normal
    warning         state
```

The ultrasonic sensor sends out a sound pulse and measures how long it takes for the echo to return.

The Arduino uses this information to calculate the distance.

When the distance is below **20 cm**, the warning system is activated.

The measured distance is also displayed in the **Serial Monitor**.

## 🚀 How to Run

1. Open `code.ino` in the Arduino IDE.
2. Connect the HC-SR04, LED, and buzzer.
3. Upload the code.
4. Open the Serial Monitor.
5. Place an object in front of the sensor.
6. Move the object closer than 20 cm.
7. Observe the LED and buzzer response.

## 🧪 Experiment

Try modifying the alarm.

### Challenge

Can you:

* Change the 20 cm threshold?
* Make the buzzer sound faster as the object gets closer?
* Add different warning tones?
* Add an LCD to display the distance?

## 📂 Files

| File       | Description         |
| ---------- | ------------------- |
| `code.ino` | Arduino source code |

📸 *Project image coming soon.*

---

### 📏 Learn → Build → Experiment
