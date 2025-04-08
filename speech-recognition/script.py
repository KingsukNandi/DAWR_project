import os
import asyncio
import speech_recognition as sr
import requests
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ESP32 server details
ESP32_IP = "192.168.52.60"
ESP32_URL = f"http://{ESP32_IP}/control-car"

# Function to send commands to ESP32
def send_esp32_command(direction, duration=None):
    try:
        payload = {"direction":direction}
        response = requests.post(ESP32_URL, json.dumps(payload, separators=(',', ':'))) # the separator is mentioned separatedly to remove all whitespaces. this is important as the esp32 webserver code that recieves this request expects the payload or the body to be void of any whitespace.
        if response.status_code != 200:
            print(f"Failed to send command: {direction}")
    except Exception as e:
        print(f"Error: {e}")

# Direction mapping dictionary
direction_mapping = {
    "forward": "W",
    "backward": "S",
    "left": "A",
    "right": "D",
    "stop": "STOP"
}

# Function to parse voice command using Groq
def parse_command_with_groq(text):
    system_prompt = """You are a robot command parser. Analyze the command and return a JSON array of actions.
    Available actions: forward, backward, left, right, stop.
    These will be mapped to: forward=W, backward=S, left=A, right=D, stop=STOP
    Include parameters like duration (seconds). 
    Example response for "Move forward for 3 seconds then turn right":
    [{"action": "forward", "duration": 3}, {"action": "right"}]"""
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        return eval(response.choices[0].message.content)
    except Exception as e:
        print(f"Groq Error: {e}")
        return None

# Function to execute sequential commands
async def execute_sequence(actions):
    for action in actions:
        # Convert action to correct direction character
        direction = direction_mapping.get(action["action"].lower(), "STOP")
        duration = action.get("duration", 0)
        
        send_esp32_command(direction)
        
        if duration > 0:
            await asyncio.sleep(duration)
            send_esp32_command("STOP")

# Function to handle general questions
def answer_general_question(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": text}],
        temperature=0.7
    )
    return response.choices[0].message.content

# Main loop
async def main():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("\nSay a command or question...")
            audio = recognizer.listen(source)
            
            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                
                if any(keyword in text for keyword in ["move", "turn", "stop", "forward"]):
                    actions = parse_command_with_groq(text)
                    if actions:
                        await execute_sequence(actions)
                else:
                    answer = answer_general_question(text)
                    print(f"Answer: {answer}")
                    
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())