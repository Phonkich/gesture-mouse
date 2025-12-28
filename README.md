# Hand-Gesture-Mouse-Controller
# Project Overview
The Hand Gesture Mouse Controller is an AI-based computer vision project that allows users to control the system mouse using real-time hand gestures. It demonstrates the practical use of AI, Computer Vision, and Human–Computer Interaction concepts.
# Features

Real-time hand gesture recognition

Touchless mouse control

AI-based hand landmark detection

Gesture-to-mouse mapping

Cursor movement, left-click, right-click, and scroll actions
# How It Works

OpenCV captures the live video feed from the webcam.

MediaPipe Hands detects and tracks hand landmarks in real time.

Hand position controls the mouse cursor movement with smoothing.

Pinch thumb and index finger for left-click.

Pinch thumb and middle finger for right-click.

Extend index and middle fingers for scroll (move hand up/down).

Mouse control is handled using the pynput and pyautogui libraries.

# Gestures Used

Move Cursor: Hand position controls cursor location (smoothed)

Left Click: Pinch thumb and index finger together

Right Click: Pinch thumb and middle finger together

Scroll: Extend index and middle fingers, move hand up/down
# Technologies & Libraries Used

Python

OpenCV

MediaPipe

pynput

pyautogui

Time module
# System Requirements

Laptop/Desktop with a webcam

Python 3.8 or above

CPU-based system (GPU not required)

Good lighting for accurate hand detection
# Installation
pip install opencv-python mediapipe pynput pyautogui

# Run the Project
python hand_gesture.py
⭐ If you like this project, feel free to star the repository!
