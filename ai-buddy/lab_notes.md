# Arduino Starter Lab notes

## The lab projects
- Week 1: Light-Activated LED (folder: week1)
- Week 2: 7-Bit Random Number Display (folder: week2)
- Week 3: Water Leak Detector (folder: week3)
- Week 4: Sound-Activated LED (folder: week4)
- Week 5: Ultrasonic Proximity Alarm (folder: week5)

## Correct Arduino facts
- pinMode(pin, mode) has only three modes: INPUT, OUTPUT, INPUT_PULLUP.
- There is no "analog" mode. analogRead(A0) works without pinMode.
- analogRead gives a number from 0 to 1023 on an Arduino Uno.
- digitalWrite(pin, HIGH) turns a pin on (5V). LOW turns it off (0V).
- Serial.begin(9600) speed must match the speed chosen in the Serial Monitor.
- An LED needs a resistor (about 220 ohms) in series, or it can burn out.

## Common beginner errors
- "was not declared in this scope": a name was used before it was created, or is misspelled.
- "expected ';' before ...": a semicolon is missing on the line above.
- Serial Monitor shows strange symbols: the baud rate does not match Serial.begin.