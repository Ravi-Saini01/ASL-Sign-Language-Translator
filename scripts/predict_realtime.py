import cv2
import numpy as np
import tensorflow as tf
import json
from collections import deque
import os

# ================= CONFIG =================
MODEL_PATH = "models/asl_cnn_model.h5"
LABEL_PATH = "models/labels.json"
CHART_PATH = "asl_chart.jpg"   # optional

IMG_SIZE = 64
CONFIDENCE_THRESHOLD = 0.80
BUFFER_SIZE = 15
# =========================================

# -------- Windows built-in Text-to-Speech --------
def speak(text):
    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"'
    )

# ---------------- Load model ----------------
model = tf.keras.models.load_model(MODEL_PATH)

with open(LABEL_PATH, "r") as f:
    class_indices = json.load(f)

labels = {v: k for k, v in class_indices.items()}

# ---------------- Load chart (optional) ----------------
chart_img = cv2.imread(CHART_PATH)
if chart_img is not None:
    chart_img = cv2.resize(chart_img, (380, 500))

# ---------------- Helper ----------------
def get_stable_label(buffer):
    if not buffer:
        return ""
    return max(set(buffer), key=buffer.count)

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0)

prediction_buffer = deque(maxlen=BUFFER_SIZE)
current_text = ""

# ---------------- UI Colors ----------------
BG_COLOR = (30, 30, 30)
GREEN = (0, 255, 0)
CYAN = (255, 255, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)
RED = (0, 0, 255)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (600, 500))

    # Background overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (600, 500), BG_COLOR, -1)
    frame = cv2.addWeighted(overlay, 0.25, frame, 0.75, 0)

    # -------- ROI --------
    roi = frame[70:320, 40:290]
    cv2.rectangle(frame, (40, 70), (290, 320), GREEN, 2)
    cv2.putText(frame, "Hand Area", (40, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2)

    roi_resized = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))
    roi_norm = roi_resized / 255.0
    roi_input = np.expand_dims(roi_norm, axis=0)

    # -------- Prediction --------
    preds = model.predict(roi_input, verbose=0)[0]
    confidence = np.max(preds)
    label = labels[np.argmax(preds)]

    if confidence > CONFIDENCE_THRESHOLD:
        prediction_buffer.append(label)

    stable_label = get_stable_label(prediction_buffer)

    # -------- UI Panels --------
    # Detected Letter Panel
    cv2.rectangle(frame, (330, 70), (580, 140), (50, 50, 50), -1)
    cv2.putText(frame, "Detected", (340, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 1)
    cv2.putText(frame, stable_label if stable_label else "-",
                (360, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, GREEN, 3)

    # Typed Text Panel
    cv2.rectangle(frame, (40, 350), (580, 430), (50, 50, 50), -1)
    cv2.putText(frame, "Typed Text", (50, 375),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 1)
    cv2.putText(frame, current_text[-20:], (50, 415),
                cv2.FONT_HERSHEY_SIMPLEX, 1, YELLOW, 2)

    # Instruction Bar
    cv2.rectangle(frame, (0, 460), (600, 500), (0, 0, 0), -1)
    cv2.putText(frame,
        "SPACE:Add Letter   BACKSPACE:Delete   S:Speak   ESC:Exit",
        (20, 490),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        CYAN,
        1
    )

    # -------- Combine with Chart --------
    if chart_img is not None:
        combined = np.hstack((frame, chart_img))
    else:
        combined = frame

    cv2.imshow("ASL Translator", combined)

    key = cv2.waitKey(1) & 0xFF

    # -------- Controls --------
    if key == 32:  # SPACEBAR
        if stable_label not in ["", "nothing", "space", "del"]:
            current_text += stable_label
            prediction_buffer.clear()

    elif key == 8:  # BACKSPACE
        current_text = current_text[:-1]

    elif key == ord('s') and current_text.strip():
        speak(current_text)

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
