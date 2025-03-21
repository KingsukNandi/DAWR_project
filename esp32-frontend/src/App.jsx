import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [direction, setDirection] = useState("");

  // Function to send direction to the backend
  const sendDirection = async (dir) => {
    try {
      const response = await fetch("http://localhost:8080/control-car", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ direction: dir }),
      });
      const result = await response.text();
      console.log(result);
    } catch (error) {
      console.error("Error sending direction:", error);
    }
  };

  // Handle keydown events
  const handleKeyDown = (event) => {
    const key = event.key.toUpperCase();
    if (
      [
        "W",
        "A",
        "S",
        "D",
        "ARROWUP",
        "ARROWDOWN",
        "ARROWLEFT",
        "ARROWRIGHT",
      ].includes(key)
    ) {
      let dir = "";
      switch (key) {
        case "W":
        case "ARROWUP":
          dir = "W";
          break;
        case "A":
        case "ARROWLEFT":
          dir = "A";
          break;
        case "S":
        case "ARROWDOWN":
          dir = "S";
          break;
        case "D":
        case "ARROWRIGHT":
          dir = "D";
          break;
        default:
          break;
      }
      setDirection(dir);
      sendDirection(dir);
    }
  };

  // Handle keyup events
  const handleKeyUp = (event) => {
    const key = event.key.toUpperCase();
    if (
      [
        "W",
        "A",
        "S",
        "D",
        "ARROWUP",
        "ARROWDOWN",
        "ARROWLEFT",
        "ARROWRIGHT",
      ].includes(key)
    ) {
      setDirection("");
      sendDirection("STOP"); // Send "STOP" when the key is released
    }
  };

  // Add event listeners for keydown and keyup
  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  // Function to handle button clicks
  const handleButtonClick = (dir) => {
    setDirection(dir);
    sendDirection(dir);
  };

  // Function to handle button release
  const handleButtonRelease = () => {
    setDirection("");
    sendDirection("STOP");
  };

  return (
    <div className="App">
      <h1>Car Controls</h1>
      <p>Current Direction: {direction || "STOP"}</p>
      <div className="controls">
        <p>Use WASD or Arrow Keys (Desktop) or Buttons (Mobile)</p>
        <div className="button-container">
          <button
            className="control-button"
            onTouchStart={() => handleButtonClick("FORWARD")}
            onTouchEnd={handleButtonRelease}
            onMouseDown={() => handleButtonClick("FORWARD")}
            onMouseUp={handleButtonRelease}
          >
            ▲
          </button>
        </div>
        <div className="button-container">
          <button
            className="control-button"
            onTouchStart={() => handleButtonClick("LEFT")}
            onTouchEnd={handleButtonRelease}
            onMouseDown={() => handleButtonClick("LEFT")}
            onMouseUp={handleButtonRelease}
          >
            ◀
          </button>
          <button
            className="control-button"
            onTouchStart={() => handleButtonClick("BACKWARD")}
            onTouchEnd={handleButtonRelease}
            onMouseDown={() => handleButtonClick("BACKWARD")}
            onMouseUp={handleButtonRelease}
          >
            ▼
          </button>
          <button
            className="control-button"
            onTouchStart={() => handleButtonClick("RIGHT")}
            onTouchEnd={handleButtonRelease}
            onMouseDown={() => handleButtonClick("RIGHT")}
            onMouseUp={handleButtonRelease}
          >
            ▶
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
