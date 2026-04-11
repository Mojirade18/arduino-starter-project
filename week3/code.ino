int waterSensor = 2;
int led = 8;

bool waterState = false;
bool lastState = false;

void setup() {
  pinMode(waterSensor, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int reading = digitalRead(waterSensor);

  // Convert to TRUE/FALSE for clarity
  waterState = (reading == HIGH);

  // Only act when state changes (prevents flicker)
  if (waterState != lastState) {
    
    if (waterState) {
      digitalWrite(led, HIGH);
      Serial.println("Water Detected!");
    } else {
      digitalWrite(led, LOW);
      Serial.println("Dry Surface");
    }

    lastState = waterState;
  }

  delay(100); // small delay for stability
}
