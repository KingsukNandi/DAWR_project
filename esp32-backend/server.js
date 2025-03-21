const express = require("express");
const cors = require("cors");
//const fetch = require("node-fetch");
const app = express();
const PORT = 8080;

app.use(cors());
app.use(express.json());

app.post("/control-car", async (req, res) => {
  const { direction } = req.body; // Get the direction (W, A, S, D, STOP)
  console.log(`Received direction: ${direction}`);

  const esp32Ip = "192.168.168.60"; // Replace with your ESP32's IP
  const url = `http://${esp32Ip}/control-car`;

  try {
    // Send a POST request to the ESP32
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ direction }), // Send the direction to the ESP32
    });
    const data = await response.text();
    console.log(`ESP32 response: ${data}`);
    res.send(`Direction: ${direction}`);
  } catch (error) {
    console.error("Error communicating with ESP32:", error);
    res.status(500).send("Failed to send direction");
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
