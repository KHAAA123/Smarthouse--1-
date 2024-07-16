int cambien = 5; // Chân cảm biến nối chân số 5 Arduino
int giatri;

void setup() {
  Serial.begin(9600);
  pinMode(cambien, INPUT);
}

void loop() {
  giatri = digitalRead(cambien); // Đọc giá trị digital từ cảm biến và gán vào biến giatri

  Serial.print("Nhà an toàn ");
  Serial.println(giatri);

  if (giatri == LOW) { // Adjust if sensor outputs LOW when detecting an obstacle
    Serial.println("Có người đột nhập"); // In ra dòng chữ "Có người đột nhập" khi cảm biến nhận tín hiệu
  }

  delay(200);
}
