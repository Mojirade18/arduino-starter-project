const int led = 8;
const int sensor_pin = A0;
int sensor;
const int threshold = 600;  // adjust after testing

void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(9600);  
}

void loop() {
  sensor = analogRead(sensor_pin);
  Serial.print("LDR Value: ");
  Serial.print(sensor);

  if (sensor < threshold) {
    // DARK → LED ON
    digitalWrite(led, HIGH);
    Serial.println(" → LED ON");
  } 
  else {
    // BRIGHT → LED OFF
    digitalWrite(led, LOW);
    Serial.println(" → LED OFF");
  }
  
  delay(200);  // small delay for stability
}
