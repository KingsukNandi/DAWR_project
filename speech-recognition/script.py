import speech_recognition as sr
import requests

# ESP32 server details
ESP32_IP = "192.168.168.60"  # Replace with your ESP32's IP address
ESP32_URL = f"http://{ESP32_IP}/control-car"

# Function to send commands to ESP32
def send_command_to_esp32(direction):
    try:
        payload = {"direction": direction}
        response = requests.post(ESP32_URL, json=payload)
        if response.status_code == 200:
            print(f"Command '{direction}' sent successfully.")
        else:
            print(f"Failed to send command. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending command: {e}")

# Function to listen for voice commands
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Speech recognition service is down.")
            return None

# Function to map voice commands to directions
def map_voice_to_direction(text):
    if "forward" in text:
        return "W"
    elif "backward" in text or "back" in text:
        return "S"
    elif "left" in text:
        return "A"
    elif "right" in text:
        return "D"
    elif "stop" in text:
        return "STOP"
    else:
        return None

# Main loop
if __name__ == "__main__":
    while True:
        print("\nSay a command (e.g., 'move forward', 'turn left', 'stop'):")
        text = listen_for_command()
        if text:
            direction = map_voice_to_direction(text)
            if direction:
                send_command_to_esp32(direction)
            else:
                print("Invalid command. Please try again.")