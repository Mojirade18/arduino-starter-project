int sensorPin = 2;   // Switch connected here
int ledPin = 8;      // LED

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  int state = digitalRead(sensorPin);

  if (state == HIGH) {        // Switch ON = "Water detected"
    digitalWrite(ledPin, HIGH);
  } else {                    // Switch OFF = "Dry"
    digitalWrite(ledPin, LOW);
  }
}
