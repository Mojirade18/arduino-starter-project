int trig = 9;
int echo = 10;
int buzzer = 8;
int led = 13;
long duration;
int distance;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  
  duration = pulseIn(echo, HIGH, 30000);
  distance = duration * 0.034 / 2;


  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  
  if (distance > 0 && distance < 20) {
    delay(200); 
    digitalWrite(led, HIGH);

 
    tone(buzzer, 736, 600);   
    delay(700);
    tone(buzzer, 586, 800);   
    delay(900);
    noTone(buzzer);

    digitalWrite(led, LOW);
    delay(2000); 
  }

  delay(200);
}
