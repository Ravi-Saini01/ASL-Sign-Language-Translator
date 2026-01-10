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
BUFFER_SIZE = 15               # majority voting frames
# =========================================

# -------- Windows built-in Text-to-Speech (NO extra installs) --------
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

# ---------------- Load ASL chart (optional) ----------------
chart_img = cv2.imread(CHART_PATH)
if chart_img is not None:
    chart_img = cv2.resize(chart_img, (400, 500))

# ---------------- Helper ----------------
def get_stable_label(buffer):
    if not buffer:
        return ""
    return max(set(buffer), key=buffer.count)

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0)

prediction_buffer = deque(maxlen=BUFFER_SIZE)
current_text = ""

print("====================================")
print(" SPACE     -> Add detected character")
print(" BACKSPACE -> Delete character")
print(" S         -> Speak text")
print(" ESC       -> Exit")
print("====================================")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # -------- ROI --------
    roi = frame[50:300, 50:300]
    cv2.rectangle(frame, (50, 50), (300, 300), (0, 255, 0), 2)

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

    # -------- Display --------
    cv2.putText(frame, f"Detected: {stable_label}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Text: {current_text}", (30, 360),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

    cv2.putText(frame,
                "SPACE=Add | BACKSPACE=Delete | S=Speak | ESC=Exit",
                (30, 420),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    frame_resized = cv2.resize(frame, (600, 500))
    combined = np.hstack((frame_resized, chart_img)) if chart_img is not None else frame_resized

    cv2.imshow("ASL Text Builder", combined)

    key = cv2.waitKey(1) & 0xFF

    # -------- Keyboard Controls --------

    # SPACEBAR → add detected character
    if key == 32:
        if stable_label not in ["", "nothing", "space", "del"]:
            current_text += stable_label
            prediction_buffer.clear()  # prevent duplicate capture

    # BACKSPACE → delete last character
    elif key == 8:
        current_text = current_text[:-1]

    # S → speak full text
    elif key == ord('s') and current_text.strip():
        speak(current_text)

    # ESC → exit
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
