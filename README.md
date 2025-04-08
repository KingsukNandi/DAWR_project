# DAWR Project: Smart Wirelessly Controlled Robot

A multi-interface robot control project that allows you to control a robot car through web interface, gesture recognition, and voice commands.

## Project Components

1. **ESP32 Machine Code**: Arduino code for ESP32 controlling robot car motors
2. **Backend Server**: Node.js server that acts as middleware between interfaces and ESP32
3. **Frontend Application**: React-based web interface for keyboard/touch controls
4. **Gesture Recognition**: Python-based hand gesture recognition system
5. **Speech Recognition**: Python-based voice command system

## Prerequisites

- Node.js (v16+) and npm
- Python (3.8+)
- Arduino IDE
- ESP32 microcontroller
- L298N motor driver
- DC motors (2x)
- Webcam (for gesture recognition)
- Microphone (for voice commands)

## Hardware Setup

1. **ESP32 and Motor Driver Connection**:
   - Connect Motor A pins:
     - Motor A1 -> GPIO26
     - Motor A2 -> GPIO27
     - Enable A -> GPIO14
   - Connect Motor B pins:
     - Motor B1 -> GPIO25
     - Motor B2 -> GPIO33
     - Enable B -> GPIO32

## Software Setup

### 1. ESP32 Configuration

1. Open `esp32-machine-code/esp32-machine-code.ino` in Arduino IDE
2. Update WiFi credentials:
   ```cpp
   const char* ssid = "your-wifi-ssid";
   const char* password = "your-wifi-password";
   ```
3. Select ESP32 board in Arduino IDE
4. Upload code to ESP32
5. Note down the IP address from Serial Monitor

### 2. Backend Server Setup

1. Navigate to backend directory:
   ```sh
   cd esp32-backend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Update ESP32 IP in `index.js`:
   ```js
   const esp32Ip = "your-esp32-ip";
   ```
4. Start server:
   ```sh
   npm start
   ```

### 3. Frontend Application Setup

1. Navigate to frontend directory:
   ```sh
   cd esp32-frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start development server:
   ```sh
   npm run dev --host
   ```

### 4. Gesture Recognition Setup

1. Navigate to gesture recognition directory:
   ```sh
   cd GestureRecognition
   ```
2. Create and activate virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run gesture recognition:
   ```sh
   python gesture_control.py
   ```

### 5. Voice Control Setup

1. Navigate to speech recognition directory:
   ```sh
   cd speech-recognition
   ```
2. Create and activate virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create `.env` file and add Groq API key:
   ```
   GROQ_API_KEY=your-groq-api-key
   ```
5. Run voice control:
   ```sh
   python script.py
   ```

## Usage Instructions

### Web Interface Control

- Access web interface at `http://localhost:5173`
- Use WASD keys or arrow keys on desktop
- Use on-screen buttons on mobile devices
- Controls:
  - W/↑: Forward
  - S/↓: Backward
  - A/←: Left
  - D/→: Right
  - Release key/button: Stop

### Gesture Control

- Hold hand in front of webcam
- Gestures:
  - All fingers up: Forward
  - Fist closed: Backward
  - Index finger up: Left
  - Pinky finger up: Right
  - Other gestures: Stop

### Voice Control

- Supported voice commands:
  - "Move forward for X seconds"
  - "Turn left/right"
  - "Stop"
  - "Move backward"

## Troubleshooting

1. **ESP32 Connection Issues**:

   - Verify WiFi credentials
   - Check if ESP32 and computer are on same network
   - Confirm ESP32 IP address in Serial Monitor
   - Check if backend server IP is correctly configured

2. **Backend Server Issues**:

   - Verify node_modules installation
   - Check if port 8080 is available
   - Ensure ESP32 IP is correctly set

3. **Gesture Recognition Issues**:

   - Check webcam connection
   - Verify Python dependencies installation
   - Ensure adequate lighting for hand detection

4. **Voice Control Issues**:
   - Check microphone connection
   - Verify Groq API key is set correctly
   - Ensure Python dependencies installation

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the ISC License.
