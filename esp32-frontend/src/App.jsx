import React, { useState } from "react";
import "./App.css";

function App() {
  const [ledState, setLedState] = useState("OFF");

  const controlLed = async (action) => {
    try {
      const response = await fetch("http://localhost:8080/control-led", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      });
      const result = await response.text();
      console.log(result);
      setLedState(action.toUpperCase());
    } catch (error) {
      console.error("Error controlling LED:", error);
    }
  };

  return (
    <div className="App">
      <h1>ESP32 LED Control</h1>
      <p>LED State: {ledState}</p>
      <button onClick={() => controlLed("on")}>Turn ON</button>
      <button onClick={() => controlLed("off")}>Turn OFF</button>
    </div>
  );
}

export default App;
