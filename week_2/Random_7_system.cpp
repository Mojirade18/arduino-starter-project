int leds[7] = {2, 3, 4, 5, 6, 7, 8};
int buttonPin = 9;
String ledNames[7] = {"Red", "Red", "Yellow", "Green", "White", "Blue", "White"};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 7; i++) {
    pinMode(leds[i], OUTPUT);
  }

  pinMode(buttonPin, INPUT);
  randomSeed(analogRead(A0)); 
}

void loop() {
  if (digitalRead(buttonPin) == HIGH) {

    int randomNumber = random(0, 128); 

    Serial.print("Random Number (Decimal): ");
    Serial.println(randomNumber);

    displayBinary(randomNumber);

    delay(500); 
  }
}

void displayBinary(int num) {
  Serial.println("LED Status:");
  for (int i = 0; i < 7; i++) {
    int bitValue = (num >> i) & 1;
    digitalWrite(leds[i], bitValue);
    
    if (bitValue == 1) {
      Serial.print(ledNames[i]);
      Serial.println(" LED is ON");
    } else {
      Serial.print(ledNames[i]);
      Serial.println(" LED is OFF");
    }
  }
  Serial.println("------------------");
}
