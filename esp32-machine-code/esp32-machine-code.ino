#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "realme 8";
const char* password = "King's Wi-Fi";

// Motor A pins
const int motorA1 = 26;
const int motorA2 = 27;
const int enableA = 14;

// Motor B pins
const int motorB1 = 25;
const int motorB2 = 33;
const int enableB = 32;

WebServer server(80); // Web server on port 80

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Set motor control pins as outputs
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
  pinMode(enableA, OUTPUT);
  pinMode(motorB1, OUTPUT);
  pinMode(motorB2, OUTPUT);
  pinMode(enableB, OUTPUT);

  // Initialize motors to stop
  stopMotors();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Define route for POST requests
  server.on("/control-car", HTTP_POST, handleControlCar);

  server.begin(); // Start the server
}

void loop() {
  server.handleClient(); // Handle incoming requests
}

// Handle POST request to control the car
void handleControlCar() {
  String requestBody = server.arg("plain"); // Get the request body
  Serial.println("Received request body: " + requestBody);

  // Parse the direction from the request body
  if (requestBody.indexOf("\"direction\":\"W\"") >= 0) {
    Serial.println("Moving FORWARD");
    moveForward();
  } else if (requestBody.indexOf("\"direction\":\"A\"") >= 0) {
    Serial.println("Moving LEFT");
    moveLeft();
  } else if (requestBody.indexOf("\"direction\":\"S\"") >= 0) {
    Serial.println("Moving BACKWARD");
    moveBackward();
  } else if (requestBody.indexOf("\"direction\":\"D\"") >= 0) {
    Serial.println("Moving RIGHT");
    moveRight();
  } else if (requestBody.indexOf("\"direction\":\"STOP\"") >= 0) {
    Serial.println("STOPPING");
    stopMotors();
  } else {
    Serial.println("Invalid direction");
  }

  server.send(200, "text/plain", "Direction received");
}

// Function to move the car forward
void moveForward() {
  digitalWrite(motorA1, HIGH);
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, HIGH);
  digitalWrite(motorB2, LOW);
  analogWrite(enableA, 255); // Full speed
  analogWrite(enableB, 255); // Full speed
}

// Function to move the car backward
void moveBackward() {
  digitalWrite(motorA1, LOW);
  digitalWrite(motorA2, HIGH);
  digitalWrite(motorB1, LOW);
  digitalWrite(motorB2, HIGH);
  analogWrite(enableA, 255); // Full speed
  analogWrite(enableB, 255); // Full speed
}

// Function to turn the car left
void moveLeft() {
  digitalWrite(motorA1, LOW);
  digitalWrite(motorA2, HIGH);
  digitalWrite(motorB1, HIGH);
  digitalWrite(motorB2, LOW);
  analogWrite(enableA, 255); // Full speed
  analogWrite(enableB, 255); // Full speed
}

// Function to turn the car right
void moveRight() {
  digitalWrite(motorA1, HIGH);
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, LOW);
  digitalWrite(motorB2, HIGH);
  analogWrite(enableA, 255); // Full speed
  analogWrite(enableB, 255); // Full speed
}

// Function to stop the car
void stopMotors() {
  digitalWrite(motorA1, LOW);
  digitalWrite(motorA2, LOW);
  digitalWrite(motorB1, LOW);
  digitalWrite(motorB2, LOW);
  analogWrite(enableA, 0); // Stop
  analogWrite(enableB, 0); // Stop
}