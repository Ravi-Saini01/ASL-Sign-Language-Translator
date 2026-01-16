import streamlit as st
import subprocess
import sys
import os

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="ASL Sign Language Translator",
    page_icon="🖐️",
    layout="centered"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}
.main {
    background-color: #f8fafc;
}
.title {
    font-size: 40px;
    font-weight: 800;
    color: #16a34a;
    text-align: center;
    margin-bottom: 5px;
}
.subtitle {
    font-size: 18px;
    color: #475569;
    text-align: center;
    margin-bottom: 30px;
}
.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 12px;
}
.text {
    font-size: 16px;
    color: #334155;
    line-height: 1.7;
}
kbd {
    background-color: #e5e7eb;
    padding: 4px 8px;
    border-radius: 6px;
    font-weight: 600;
}
.footer {
    text-align: center;
    color: #64748b;
    font-size: 14px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.markdown('<div class="title">🖐️ ASL Sign Language Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ASL → Text & Speech (Camera-Based)</div>', unsafe_allow_html=True)

# ---------------- Instructions ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📌 How to Use</div>', unsafe_allow_html=True)
st.markdown("""
<div class="text">
1️⃣ Show ASL hand signs clearly inside the green box<br>
2️⃣ Hold the sign steady until it is detected<br>
3️⃣ Press <kbd>SPACE</kbd> to add the detected character<br>
4️⃣ Press <kbd>BACKSPACE</kbd> to remove the last character<br>
5️⃣ Press <kbd>S</kbd> to speak the full sentence<br>
6️⃣ Press <kbd>ESC</kbd> to stop the camera
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Start Button ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Start Translation</div>', unsafe_allow_html=True)

if st.button("▶ Start ASL Translator", use_container_width=True):
    if not os.path.exists("models/asl_cnn_model.h5"):
        st.error("❌ Model file not found. Please train the model once.")
    else:
        st.success("📷 Camera started. Check the OpenCV window.")
        subprocess.run([sys.executable, "scripts/predict_realtime.py"])

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Supported Signs ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧠 Supported Signs</div>', unsafe_allow_html=True)
st.markdown("""
<div class="text">
✔ Alphabets: A – Z<br>
✔ Space (via keyboard)<br>
✔ Delete (Backspace)<br>
✔ Nothing (idle hand)<br><br>
⚠️ This system supports <b>static ASL gestures only</b>.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown('<div class="footer">Academic Project • ASL Sign Language Translator</div>', unsafe_allow_html=True)
