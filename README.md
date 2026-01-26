<h1>🖐️ ASL Sign Language Translator</h1>

ASL → Text & Speech (Camera-Based)

A real-time American Sign Language (ASL) Translator that converts ASL hand gestures into readable text and spoken speech using a webcam.
The system is trained on the Kaggle ASL Alphabet Dataset and provides a modern Streamlit interface for easy interaction.

This project is designed for academic use, final-year demos, and resume portfolios.

🚀 Features

📷 Real-time ASL recognition using webcam

🧠 CNN-based deep learning model

⌨️ Keyboard-controlled character capture

📝 Word & sentence formation

🔊 Text-to-Speech output (no external media player)

🎨 Clean, modern Streamlit UI

📊 Stable prediction using majority voting

❌ No retraining required during use

<h1>🧠 How It Works (Pipeline)</h1>
Webcam
   ↓
Hand Image (ROI)
   ↓
CNN Model (Trained on ASL Dataset)
   ↓
Stable Prediction (Majority Voting)
   ↓
Keyboard-Controlled Text Builder
   ↓
Text-to-Speech Output

<h1>📊 Dataset</h1>
Source: Kaggle – ASL Alphabet Dataset

Classes: 29

A–Z

space

delete

nothing

Images: ~87,000

Type: Static ASL gestures

🔗 Dataset link:
https://www.kaggle.com/datasets/grassknoted/asl-alphabet

<h1>🏗 Project Structure</h1>

ASL-Sign-Language-Translator/
│
├── dataset/
│   └── asl_alphabet/
│
├── models/
│   ├── asl_cnn_model.h5
│   └── labels.json
│
├── scripts/
│   └── predict_realtime.py
│
├── asl_chart.jpg
├── app.py
├── requirements.txt
└── README.md

<h1>⚙️ Technologies Used</h1>

Python

TensorFlow / Keras

OpenCV

NumPy

Streamlit

Windows Speech API (Text-to-Speech)

<h1>⌨️ Controls & Usage</h1>

<b>Key</b>	                    <b>Action</b>

<b>SPACEBAR</b>	                Add detected ASL character<>
<b>BACKSPACE</b>	            Delete previous character
<b>S</b>	                    Speak the full sentence
<b>ESC</b>	                    Exit camera window

👉 Characters are added only when SPACEBAR is pressed to avoid accidental input.

<h1>▶️ How to Run the Project</h1>

<h2>1️⃣ Install Dependencies</h2>
pip install -r requirements.txt

<h2>2️⃣ Ensure Model Files Exist</h2>
models/
├── asl_cnn_model.h5
└── labels.json

<h2>3️⃣ Run the Application</h2>
streamlit run app.py

<h1>🖥 User Interface</h1>
Modern card-based Streamlit UI

Clear instructions and controls

OpenCV window for live camera feed

Optional ASL alphabet chart displayed alongside camera

<h1>🧪 Stability Improvements</h1>
To ensure accurate word formation:

✔ Confidence thresholding

✔ Majority voting across multiple frames

✔ Keyboard-controlled character capture

This prevents:

Early detection

Flickering predictions

Repeated or wrong characters

<h1>⚠️ Limitations</h1>
Supports static ASL gestures only

Dynamic gestures (J, Z) are not covered

Facial expressions are not included

Works best with good lighting and plain background

<h1>📜 License</h1>
This project is intended for educational and academic use only.


