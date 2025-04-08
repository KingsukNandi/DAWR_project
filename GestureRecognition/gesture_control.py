import cv2
import mediapipe as mp
import numpy as np
import requests  # Import requests to send HTTP requests
import threading

# Initialize Mediapipe Hand Module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Backend Server URL (Node.js)
BACKEND_URL = "http://localhost:8080/control-car"

# Function to determine gesture
def get_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Check if fingers are up
    index_finger_up = index_tip[1] < landmarks[6][1]
    middle_finger_up = middle_tip[1] < landmarks[10][1]
    ring_finger_up = ring_tip[1] < landmarks[14][1]
    pinky_finger_up = pinky_tip[1] < landmarks[18][1]
    thumb_extended = thumb_tip[0] > landmarks[3][0]  # X-coordinate for thumb

    # Define gestures
    if index_finger_up and middle_finger_up and ring_finger_up and pinky_finger_up and thumb_extended:
        return "W"  # Move Forward
    elif not index_finger_up and not middle_finger_up and not ring_finger_up and not pinky_finger_up and not thumb_extended:
        return "S"  # Move Backward
    elif index_finger_up and not middle_finger_up and not ring_finger_up and not pinky_finger_up:
        return "A"  # Move Left
    elif pinky_finger_up and not index_finger_up and not middle_finger_up and not ring_finger_up:
        return "D"  # Move Right
    else:
        return "STOP"  # No Stop condition (one gesture must always be detected)

# Function to send request to backend
def send_command(direction):
    if direction:
        try:
            response = requests.post(BACKEND_URL, json={"direction": direction})
            print(f"Sent {direction} | Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")


# Open webcam
cap = cv2.VideoCapture(0)
window_closed = False  # Track if window is closed

while (cap.isOpened() and not window_closed):
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Convert to numpy array for easier calculations
            landmarks = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark])
            
            # Detect gesture
            gesture = get_gesture(landmarks)  
            
            
            # Send command to backend in a separate thread
            if gesture:
                thread = threading.Thread(target=send_command, args=(gesture,))
                thread.start()  # Start the thread to send command       
            print(f"Detected: {gesture}")

            # Display text on screen
            cv2.putText(frame, f"Gesture: {gesture}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Control", frame)

    # Capture key press events
    key = cv2.waitKey(1) & 0xFF

    # If the window is closed, `cv2.getWindowProperty` may not detect it immediately.
    # Instead, check if `cv2.waitKey()` returned -1 (which means no window is open).
    if key == ord("q"):
        print("Q key pressed. Exiting...")
        break

    if cv2.getWindowProperty("Hand Gesture Control", cv2.WND_PROP_AUTOSIZE) >= 0:
        continue  # Window is still open, continue the loop
    else:
        print("Window closed manually. Exiting...")
        break



# Release resources after loop ends
cap.release()
cv2.destroyAllWindows()
