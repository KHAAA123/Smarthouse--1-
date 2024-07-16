int ledPin1 = 3;
int ledPin2 = 2;
int ledPin3 = 4; 
int fanPin = 5; // Chân điều khiển quạt
String command = "";

void setup() {
  Serial.begin(9600);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT); 
  pinMode(ledPin3, OUTPUT); 
  pinMode(fanPin, OUTPUT); // Thiết lập chân quạt là OUTPUT
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(fanPin, LOW); // Tắt quạt ban đầu
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
  }
}