#include <WiFi.h>
#include <WebServer.h>

// Replace with your network credentials
const char* ssid = "realme 8";
const char* password = "King's Wi-Fi";

// Create an instance of the web server
WebServer server(80);

// Assign output variables to GPIO pins
const int ledPin = 2;  // Built-in LED on GPIO 2

void setup() {
  // Initialize the output variables as outputs
  pinMode(ledPin, OUTPUT);
  // Set outputs to LOW (LED off by default)
  digitalWrite(ledPin, LOW);

  // Start Serial Monitor
  Serial.begin(115200);
  delay(1000);  // 1-second delay after Serial.begin()

  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Define API endpoint
  server.on("/control-led", HTTP_POST, handleControlLed);

  // Start the server
  server.begin();
}

void loop() {
  // Handle incoming client requests
  server.handleClient();
}

// Handle POST request to control the LED
void handleControlLed() {
  // Parse the request body
  String requestBody = server.arg("plain");
  Serial.println("Received request body: " + requestBody);

  // Parse the JSON payload
  if (requestBody.indexOf("\"action\":\"on\"") >= 0) {
    digitalWrite(ledPin, HIGH);  // Turn LED on
    server.send(200, "text/plain", "LED turned ON");
  } else if (requestBody.indexOf("\"action\":\"off\"") >= 0) {
    digitalWrite(ledPin, LOW);  // Turn LED off
    server.send(200, "text/plain", "LED turned OFF");
  } else {
    server.send(400, "text/plain", "Invalid action");
  }
}