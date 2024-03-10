#include <Servo.h>

Servo myServo;
int motorPin = 9;

void setup() {
  Serial.begin(9600);
  myServo.attach(motorPin);
}

void loop() {
  if (Serial.available() > 0) {
    String val = Serial.readString();
    if (val == "1") {
      myServo.write(90);
    } else {
      myServo.write(60);
    }
  }
  delay(1000);
}
