#include "BluetoothSerial.h"
BluetoothSerial SerialBT; // Create a Bluetooth serial object

// Pin assignments for motors
int leftEnable = 16;
int leftInput1 = 17;
int leftInput2 = 18;

int rightEnable = 19;
int rightInput1 = 21;
int rightInput2 = 22;

int fanInput1 = 25;
int fanInput2 = 26;

unsigned long lastCommandTime = 0; // Store the last time a command was received
const unsigned long timeout = 100; // Time after which the motors stop if no command is received (100ms)

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_Robot"); // Bluetooth name
  
  // Motor pins as outputs
  pinMode(leftEnable, OUTPUT);
  pinMode(leftInput1, OUTPUT);
  pinMode(leftInput2, OUTPUT);
  
  pinMode(rightEnable, OUTPUT);
  pinMode(rightInput1, OUTPUT);
  pinMode(rightInput2, OUTPUT);
  
  pinMode(fanInput1, OUTPUT);
  pinMode(fanInput2, OUTPUT);
  
  Serial.println("Bluetooth ready, waiting for commands...");
}

void loop() {
  if (SerialBT.available()) {
    char command = SerialBT.read();
    
    switch(command) {
      // Move forward on press 'w'
      case 'w':
        moveForward();
        break;

      // Move backward on press 's'
      case 's':
        moveBackward();
        break;

      // Turn left on press 'a'
      case 'a':
        turnLeft();
        break;

      // Turn right on press 'd'
      case 'd':
        turnRight();
        break;

      // Turn fan on with 'f'
      case 'f':
        turnFanOn();
        break;

      // Turn fan off with 'o'
      case 'o':
        turnFanOff();
        break;

      default:
        stopMotors();
        break;
    }
    lastCommandTime = millis(); // Update the time when the command was received
  }

  // Stop the motors if no command was received for a certain time
  if (millis() - lastCommandTime > timeout) {
    stopMotors();  // Stop motors after timeout
  }
}

// Motor control functions
void moveForward() {
  digitalWrite(leftEnable, HIGH);
  digitalWrite(leftInput1, HIGH);
  digitalWrite(leftInput2, LOW);
  
  digitalWrite(rightEnable, HIGH);
  digitalWrite(rightInput1, HIGH);
  digitalWrite(rightInput2, LOW);
}

void moveBackward() {
  digitalWrite(leftEnable, HIGH);
  digitalWrite(leftInput1, LOW);
  digitalWrite(leftInput2, HIGH);
  
  digitalWrite(rightEnable, HIGH);
  digitalWrite(rightInput1, LOW);
  digitalWrite(rightInput2, HIGH);
}

void turnLeft() {
  digitalWrite(leftEnable, HIGH);
  digitalWrite(leftInput1, LOW);
  digitalWrite(leftInput2, HIGH);

  digitalWrite(rightEnable, HIGH);
  digitalWrite(rightInput1, HIGH);
  digitalWrite(rightInput2, LOW);
}

void turnRight() {
  digitalWrite(leftEnable, HIGH);
  digitalWrite(leftInput1, HIGH);
  digitalWrite(leftInput2, LOW);
  
  digitalWrite(rightEnable, HIGH);
  digitalWrite(rightInput1, LOW);
  digitalWrite(rightInput2, HIGH);
}

void stopMotors() {
  digitalWrite(leftEnable, LOW);
  digitalWrite(rightEnable, LOW);
}

void turnFanOn() {
  digitalWrite(fanInput1, HIGH);
  digitalWrite(fanInput2, LOW);
}

void turnFanOff() {
  digitalWrite(fanInput1, LOW);
  digitalWrite(fanInput2, LOW);
}
