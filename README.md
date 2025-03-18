# DAWR Project

This project consists of three main components:

1. **ESP32 Machine Code**: Code to run on the ESP32 microcontroller.
2. **Backend Server**: Node.js server to communicate with the ESP32.
3. **Frontend Application**: React application to control the LED on the ESP32.

## Prerequisites

- Node.js and npm installed on your machine.
- Arduino IDE for uploading code to the ESP32.
- ESP32 microcontroller.

## Setup Instructions

### 1. ESP32 Machine Code

1. Open the `esp32-machine-code.ino` file in the Arduino IDE.
2. Update the `ssid` and `password` variables with your Wi-Fi credentials.
3. Connect your ESP32 to your computer.
4. Select the appropriate board and port in the Arduino IDE.
5. Upload the code to the ESP32.

### 2. Backend Server

1. Navigate to the `esp32-backend` directory:
   ```sh
   cd c:\Users\Kingsuk Nandi\Documents\my_workspace\DAWR_project\esp32-backend
   ```
2. Install the dependencies:
   ```sh
   npm install
   ```
3. Update the `esp32Ip` variable in `server.js` with the IP address of your ESP32.
4. Start the backend server:
   ```sh
   npm start
   ```

### 3. Frontend Application

1. Navigate to the `esp32-frontend` directory:
   ```sh
   cd c:\Users\Kingsuk Nandi\Documents\my_workspace\DAWR_project\esp32-frontend
   ```
2. Install the dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```

## Usage

1. Ensure the ESP32 is connected to your Wi-Fi network.
2. Start the backend server.
3. Start the frontend application.
4. Open your browser and navigate to `http://localhost:3000`.
5. Use the buttons on the web page to control the LED on the ESP32.

## Troubleshooting

- Ensure the ESP32 is connected to the same network as your computer.
- Check the serial monitor in the Arduino IDE for any connection issues.
- Verify the IP address of the ESP32 and update it in the backend server code if necessary.
