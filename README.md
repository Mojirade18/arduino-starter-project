# 🔧 Arduino Starter Lab

> **Learn → Build → Experiment → Contribute**

A beginner-friendly collection of hands-on **Arduino and embedded systems projects** designed to help learners move from basic electronics and Arduino programming to more practical embedded systems concepts.

This repository is also a space for beginners to **practice GitHub, collaborate, document their work, and make meaningful open-source contributions.**

---

## 📚 Learning Path

The projects are organized as a weekly learning journey. Each project introduces new components, programming concepts, and problem-solving skills.

| Week  | Project                               | What You'll Learn                             | Preview                                                             |
| ----- | ------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------- |
| **1** | 💡 Light-Activated LED                | LDR sensors, analog input, thresholds         | ![Light-Activated LED](week1/smart_light.BMP)                       |
| **2** | 🔢 7-Bit Random Number Binary Display | Binary numbers, LEDs, buttons, random numbers | ![7-Bit Random Number Display](week2/photo_2026-02-20_20-10-31.jpg) |
| **3** | 💧 Water Leak Detector                | Water sensors, digital input, state changes   | ![Water Leak Detector](week3/photo_2026-03-17_22-25-05.jpg)         |
| **4** | 👏 Sound-Activated LED                | Sound sensors, timing, event detection        | ![Sound-Activated LED](week4/photo_2026-03-29_21-16-15.jpg)         |
| **5** | 📏 Ultrasonic Proximity Alarm         | Distance measurement, HC-SR04, buzzer alerts  | Coming soon                                                         |

---

# 🚀 Projects

## Week 1 — 💡 Light-Activated LED

### What it does

The Light-Activated LED uses an **LDR (Light Dependent Resistor)** to detect the surrounding light level.

The Arduino reads the LDR value and compares it against a predefined threshold.

* 🌙 When it is dark → **LED turns ON**
* ☀️ When it is bright → **LED turns OFF**
* 🖥️ LDR readings are displayed on the Serial Monitor

### Concepts

* Analog input
* LDR sensors
* Threshold values
* Digital output
* Serial communication
* Basic `if/else` logic

### Components

* Arduino
* LDR
* LED
* Resistor
* Jumper wires
* Breadboard

### Files

```text
week1/
├── code.ino
├── smart_light.BMP
├── smart_light.dsn
└── smart_light.pdsprj
```

### Preview

![Light-Activated LED](week1/smart_light.BMP)

---

## Week 2 — 🔢 7-Bit Random Number Binary Display

### What it does

This project generates a random number between **0 and 127** whenever a button is pressed.

The generated number is then converted into binary and displayed using **7 LEDs**, with each LED representing one binary bit.

The decimal value and LED states are also printed to the Serial Monitor.

### Example

If the generated number is:

```text
5
```

Its 7-bit binary representation is:

```text
0000101
```

The corresponding LEDs represent the individual bits.

### Concepts

* Binary numbers
* Bit representation
* LEDs
* Push buttons
* Random number generation
* Digital output
* Serial Monitor

### Components

* Arduino
* 7 LEDs
* 7 resistors
* Push button
* Breadboard
* Jumper wires

### Files

```text
week2/
├── code.ino
├── photo_2026-02-20_20-10-31.jpg
├── photo_2026-02-20_20-10-40.jpg
├── photo_2026-02-20_20-10-48.jpg
└── smart_light (2).dsn
```

### Preview

![7-Bit Random Number Display](week2/photo_2026-02-20_20-10-31.jpg)

---

## Week 3 — 💧 Water Leak Detector

### What it does

The Water Leak Detector monitors a water sensor and detects when water is present.

When water is detected:

* 💧 The Arduino detects the change
* 💡 The LED turns ON
* 🖥️ `Water Detected!` is displayed on the Serial Monitor

When the surface becomes dry:

* LED turns OFF
* 🖥️ `Dry Surface` is displayed

The project also includes a **simulation version** that uses a switch instead of the physical water sensor for testing in Proteus.

### Concepts

* Sensors
* Digital input
* State changes
* Conditional statements
* Serial communication
* Hardware simulation

### Components

* Arduino
* Water sensor
* LED
* Resistor
* Jumper wires
* Breadboard

### Files

```text
week3/
├── code.ino
├── code_simulation.ino
├── photo_2026-03-17_22-25-05.jpg
└── photo_2026-03-17_22-25-32.jpg
```

### Preview

![Water Leak Detector](week3/photo_2026-03-17_22-25-05.jpg)

---

## Week 4 — 👏 Sound-Activated LED

### What it does

The Sound-Activated LED uses a sound sensor module to detect a clap or sudden sound.

When a sound is detected:

1. The Arduino detects the sound signal.
2. The LED turns ON.
3. The LED remains ON for approximately **2 seconds**.
4. The LED turns OFF.

### Concepts

* Sound sensors
* Digital signals
* Event detection
* Timing
* `delay()`
* Digital output

### Components

* Arduino
* Sound sensor module
* LED
* Resistor
* Breadboard
* Jumper wires

### Files

```text
week4/
├── code.ino
├── photo_2026-03-17_22-25-05 (1).jpg
└── photo_2026-03-29_21-16-15.jpg
```

### Preview

![Sound-Activated LED](week4/photo_2026-03-29_21-16-15.jpg)

---

## Week 5 — 📏 Ultrasonic Proximity Alarm

### What it does

The Ultrasonic Proximity Alarm uses an **HC-SR04 ultrasonic sensor** to measure the distance between the sensor and an object.

When an object moves closer than **20 cm**, the system activates an alert.

### System behaviour

```text
Object detected
       ↓
Measure distance
       ↓
Is distance < 20 cm?
       ↓
      YES
       ↓
LED turns ON
       ↓
Buzzer produces warning tone
       ↓
Urgent tone
       ↓
Pause
       ↓
Measure again
```

The measured distance is also displayed on the Serial Monitor.

### Concepts

* Ultrasonic sensors
* Distance measurement
* Echo/trigger signals
* Buzzer control
* Conditional logic
* Multiple-tone alerts
* Serial monitoring

### Components

* Arduino
* HC-SR04 ultrasonic sensor
* LED
* Buzzer
* Resistor
* Breadboard
* Jumper wires

### Files

```text
week5/
└── code.ino
```

> 📸 **Project image coming soon.**

---

# 🛠️ Hardware & Software

## Hardware

The projects in this repository use beginner-friendly electronic components such as:

* Arduino boards
* LEDs
* Resistors
* Push buttons
* LDR sensors
* Water sensors
* Sound sensors
* Ultrasonic sensors
* Buzzers
* Breadboards
* Jumper wires

More components will be introduced as the learning path grows.

## Software

Recommended tools include:

* **Arduino IDE** — writing and uploading Arduino programs
* **Proteus** — circuit simulation
* **GitHub** — version control and collaboration

---

# 💻 Getting Started

You don't need advanced embedded systems knowledge to start.

### 1. Clone or download the repository

You can download this repository and work through the projects at your own pace.

### 2. Choose a project

Start from **Week 1** and gradually work your way through the learning path.

### 3. Open the Arduino code

Open the project's `.ino` file using the Arduino IDE.

### 4. Build the circuit

Use the circuit information and project files to recreate the hardware setup.

### 5. Upload the code

Connect your Arduino board and upload the program.

### 6. Experiment

Don't just copy the code.

Try changing:

* Threshold values
* Timing
* LED behaviour
* Sensor sensitivity
* Alert conditions
* Output messages

### 7. Break it and fix it

Making mistakes is part of the learning process.

---

# 🎯 Learning Philosophy

This repository follows a simple approach:

```text
LEARN
  ↓
BUILD
  ↓
EXPERIMENT
  ↓
BREAK
  ↓
DEBUG
  ↓
UNDERSTAND
  ↓
CONTRIBUTE
```

The goal isn't just to collect Arduino projects.

The goal is to understand **why the hardware and software work together**.

---

# 🌱 Beginner Challenges

As the repository grows, beginner-friendly challenges will be added so contributors can practice what they learn.

Planned challenges include:

* 💡 Blink Without Delay
* 🚦 Traffic Light
* 🔘 Button Counter
* 🌙 Automatic Night Light
* 🌡️ Temperature Monitor
* ⚡ Reaction Time Game

Challenges will gradually increase in difficulty.

---

# 🤝 Contributing

Contributions are welcome!

You don't need to be an embedded systems expert to contribute.

You can contribute by:

* Fixing documentation
* Improving existing code
* Adding explanations
* Testing a project
* Reporting bugs
* Improving circuit diagrams
* Adding beginner challenges
* Adding new Arduino projects
* Helping other beginners
* Improving the README
* Suggesting project ideas

If this is your **first open-source contribution**, that's completely fine.

This repository is designed to help beginners learn while contributing.

> **You don't have to be an expert to contribute. You just have to be willing to learn.**

More detailed contribution guidelines will be available in `CONTRIBUTING.md`.

---

# 🗺️ Roadmap

### ✅ Current

* [x] Week 1 — Light-Activated LED
* [x] Week 2 — 7-Bit Random Number Binary Display
* [x] Week 3 — Water Leak Detector
* [x] Week 4 — Sound-Activated LED
* [x] Week 5 — Ultrasonic Proximity Alarm

### 🔨 Improving

* [ ] Add individual project README files
* [ ] Clean and standardize project filenames
* [ ] Add circuit diagrams
* [ ] Add wiring explanations
* [ ] Add beginner challenges
* [ ] Create contribution guidelines
* [ ] Add issue templates
* [ ] Add pull request template
* [ ] Add Code of Conduct
* [ ] Add GitHub Actions
* [ ] Create beginner-friendly issues
* [ ] Build a contributor pathway

### 🚀 Future

* [ ] ESP32 projects
* [ ] IoT projects
* [ ] Embedded C/C++
* [ ] Sensor projects
* [ ] Robotics projects
* [ ] More advanced embedded systems projects
* [ ] Community-built projects

---

# 🏆 Contributor Journey

This project aims to help contributors progress gradually:

```text
GitHub Beginner
      ↓
Arduino Beginner
      ↓
Embedded Systems Beginner
      ↓
Project Contributor
      ↓
Open Source Contributor
```

You can start by fixing a typo or improving documentation and eventually contribute complete embedded systems projects.

---

# 📸 Project Gallery

As more projects are added, this section will become a visual gallery of the circuits and builds created throughout the learning journey.

More project images coming soon.

---

# ⭐ Support the Project

If you find this repository useful:

⭐ Star the repository

🍴 Fork it

🐛 Report an issue

💡 Suggest an improvement

🤝 Make a contribution

📢 Share it with someone learning Arduino or embedded systems.

Every contribution helps make the project better for the next beginner.

---

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

## 💬 Final Note

This repository is more than a collection of Arduino code.

It is a **learning laboratory for embedded systems and open source**.

Whether you're making your first LED blink, learning how sensors work, experimenting with Arduino, or making your first GitHub contribution, you're welcome here.

### 🔧 Learn → Build → Experiment → Contribute
