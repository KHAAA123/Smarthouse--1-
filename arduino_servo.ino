#include <Servo.h>

int ledPin1 = 3;
int ledPin2 = 2;
int ledPin3 = 4;
int fanPin = 5;
  int servoPin = 6; 
String command = "";
Servo myServo; 

const int IR_PIN = 12;    
const int LOA = 11;
const int HONGNGOAI = 10;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(fanPin, OUTPUT);
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(fanPin, LOW); 

  myServo.attach(servoPin); 
  myServo.write(0); 

  pinMode(IR_PIN, INPUT);   
  pinMode(LOA, OUTPUT); 
  digitalWrite(LOA, LOW);
  pinMode(HONGNGOAI, INPUT); 
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim();
  }

  // Điều khiển đèn
  if (command == "L1ON") {
    digitalWrite(ledPin1, HIGH);
  } else if (command == "L1OFF") {
    digitalWrite(ledPin1, LOW);
  } else if (command == "L2ON") {
    digitalWrite(ledPin2, HIGH);
  } else if (command == "L2OFF") {
    digitalWrite(ledPin2, LOW);
  } else if (command == "L3ON") {
    digitalWrite(ledPin3, HIGH);
  } else if (command == "L3OFF") {
    digitalWrite(ledPin3, LOW);

  // Điều khiển quạt
  } else if (command == "FANON") {
    digitalWrite(fanPin, HIGH);
  } else if (command == "FANOFF") {
    digitalWrite(fanPin, LOW);

  // Điều khiển servo
  } else if (command == "D1ON") {
    myServo.write(180); // Mở cửa
  } else if (command == "D1OFF") {
    myServo.write(0); // Đóng cửa
  }


  int irValue = digitalRead(IR_PIN);

  if (irValue == LOW) { 
    for (int i = 0; i < 10; i++) { 
      digitalWrite(ledPin1, HIGH);
      delay(100);
      digitalWrite(ledPin1, LOW);
      digitalWrite(ledPin2, HIGH);
      delay(100);
      digitalWrite(ledPin2, LOW);
      digitalWrite(ledPin3, HIGH);
      delay(100);
      digitalWrite(ledPin3, LOW);
    }
  }

  delay(50);
  
  
  int irValue2 = digitalRead(HONGNGOAI); 

  if (irValue2 == LOW) { 
    for (int i = 0; i < 10; i++) { 
      digitalWrite(LOA, HIGH);
      delay(50);
      digitalWrite(LOA, LOW);
      delay(50);
      digitalWrite(ledPin1, HIGH);
      delay(50);
      digitalWrite(ledPin1, LOW);
      delay(50);

    }
  }

  delay(50);
}
