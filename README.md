# Virtual Mouse using Hand Gestures

A computer vision–based virtual mouse system that enables real-time cursor control using hand gestures captured through a webcam. Built using MediaPipe hand tracking, OpenCV, and PyAutoGUI for touchless human-computer interaction.

---

## Features

- Real-time hand tracking using 21 landmark detection
- Smooth cursor movement with gesture control
- Gesture-based mouse clicking
- Scroll control using multi-finger gestures
- Dynamic cursor trail visualization
- Touchless interaction through webcam input

---

## Gesture Controls

| Gesture | Fingers Up | Action |
|----------|-------------|--------|
| Move Cursor | Index Finger | Smooth cursor movement |
| Click | Index + Middle | Click when fingertips touch |
| Scroll | Index + Middle + Ring | Scroll up/down based on hand position |

---

## Tech Stack

- MediaPipe — Hand landmark detection
- OpenCV — Webcam frame processing
- PyAutoGUI — Mouse automation
- NumPy — Numerical operations

---

## Project Structure

```bash
Virtual-Mouse/
├── AIvirtualmouseproject.py
├── Handtracking.py
├── requirements.txt
└── README.md
```

---

## Requirements

```text
mediapipe==0.8.3.1
numpy==1.20.2
opencv-python
pyautogui
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the main application:

```bash
python AIvirtualmouseproject.py
```

Ensure webcam access is enabled before running the program.

---

## Author

Khushi Yadav
