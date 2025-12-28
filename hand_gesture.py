# HAND GESTURE MOUSE CONTROLLER

import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller as MouseController
import pyautogui
import time

mouse = MouseController()
screen_width, screen_height = pyautogui.size()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pTime = 0
active_action = "Idle"

clicking = False
prev_mouse_x = None
prev_mouse_y = None
smoothing_factor = 0.3  # Adjust for smoothness (0.1 very smooth, 1.0 no smoothing)

def fingers_extended(hand):
    extended = []
    extended.append(hand.landmark[4].y < hand.landmark[3].y)  # thumb
    for tip in [8, 12, 16, 20]:  # index, middle, ring, pinky
        extended.append(hand.landmark[tip].y < hand.landmark[tip - 2].y)
    return extended


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        thumb = hand.landmark[4]
        index = hand.landmark[8]

        # Map hand position to mouse position
        current_mouse_x = int(index.x * screen_width)
        current_mouse_y = int(index.y * screen_height)

        # Apply smoothing
        if prev_mouse_x is None:
            mouse_x = current_mouse_x
            mouse_y = current_mouse_y
        else:
            mouse_x = int(prev_mouse_x * (1 - smoothing_factor) + current_mouse_x * smoothing_factor)
            mouse_y = int(prev_mouse_y * (1 - smoothing_factor) + current_mouse_y * smoothing_factor)

        prev_mouse_x = mouse_x
        prev_mouse_y = mouse_y

        mouse.position = (mouse_x, mouse_y)

        extended = fingers_extended(hand)

        # Detect scroll: if index and middle extended, others not
        if extended[1] and extended[2] and not extended[0] and not extended[3] and not extended[4]:
            if index.y < 0.3:
                pyautogui.scroll(1)
                active_action = "Scroll Up"
            elif index.y > 0.7:
                pyautogui.scroll(-1)
                active_action = "Scroll Down"
            else:
                active_action = "Scroll Mode"
        else:
            # Detect left click: if thumb and index are close
            left_distance = ((thumb.x - index.x)**2 + (thumb.y - index.y)**2)**0.5
            # Detect right click: if thumb and middle are close
            middle = hand.landmark[12]
            right_distance = ((thumb.x - middle.x)**2 + (thumb.y - middle.y)**2)**0.5

            if left_distance < 0.05:
                if not clicking:
                    mouse.click(Button.left, 1)
                    clicking = True
                    active_action = "Left Click"
            elif right_distance < 0.05:
                if not clicking:
                    mouse.click(Button.right, 1)
                    clicking = True
                    active_action = "Right Click"
            else:
                clicking = False
                active_action = "Moving"
    else:
        active_action = "Idle"


    cTime = time.time()
    fps = 1 / (cTime - pTime) if pTime != 0 else 0
    pTime = cTime

    cv2.putText(image, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.putText(image, f'Action: {active_action}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

