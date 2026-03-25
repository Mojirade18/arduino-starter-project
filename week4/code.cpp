int soundSensor = 2;   
int LED = 8;          

void setup() {
  pinMode(soundSensor, INPUT);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);  
}

void loop() {
  int SensorData = digitalRead(soundSensor);

  if (SensorData == HIGH) {   
    digitalWrite(LED, HIGH);  
    delay(2000);              
    digitalWrite(LED, LOW);   
  }
}
