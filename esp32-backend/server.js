const express = require("express");
const cors = require("cors"); // Import CORS
const app = express();
const PORT = 8080;

// Enable CORS for all routes
app.use(cors());

// Middleware to parse JSON and form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Endpoint to control the LED
app.post("/control-led", (req, res) => {
  const { action } = req.body; // action can be "on" or "off"
  console.log(`Received request to turn LED ${action}`);

  // Send a request to the ESP32
  const esp32Ip = "192.168.168.178"; // Replace with your ESP32's IP
  const url = `http://${esp32Ip}/control-led`;

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action }),
  })
    .then((response) => response.text())
    .then((data) => {
      console.log(`ESP32 response: ${data}`);
      res.send(`LED turned ${action}`);
    })
    .catch((error) => {
      console.error("Error communicating with ESP32:", error);
      res.status(500).send("Failed to control LED");
    });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
