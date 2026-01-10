import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="ASL Translator", layout="centered")

st.title("🖐️ ASL Sign Language Translator")
st.markdown("### ASL → Text & Speech (Camera-Based)")

st.divider()

st.markdown("""
**Instructions:**
1. Click **Start Translator**
2. Show ASL hand signs inside the green box
3. Detected sign will be spoken aloud
4. Press **ESC** to stop the camera
""")

st.divider()

if st.button("▶ Start Translator", use_container_width=True):
    st.info("Starting webcam... Press ESC to stop.")
    subprocess.run([sys.executable, "scripts/predict_realtime.py"])

st.divider()

st.markdown("""
**Supported Signs**
- A–Z  
- space  
- delete  
- nothing  

**Noteee:** This system supports **static ASL gestures only**.
""")
