import streamlit as st
import time

from mic import record_until_silence, voice_available
from stt import transcribe
from chat import ask
from voice import speak

st.set_page_config(page_title="Emma", layout="centered")

# -------------------------
# CSS (Jarvis style)
# -------------------------
st.markdown("""
<style>
.body { height:100dvh; width:100dvw; background:black; color:#00ffff; display: flex; align-item: center; justify-content: center}
.core {
  width:200px;height:200px;border-radius:50%;
  border:4px solid #00ffff;margin:auto;
  animation:pulse 2s infinite;
}
.listening { border-color:#00ff00; }
.thinking { border-color:#ffff00; }
.speaking { border-color:#ff00ff; }
@keyframes pulse {
  0%{box-shadow:0 0 10px}
  50%{box-shadow:0 0 30px}
  100%{box-shadow:0 0 10px}
}
.status { text-align:center;font-size:20px;margin-top:10px }
</style>
""", unsafe_allow_html=True)

# -------------------------
# STATE
# -------------------------
if "state" not in st.session_state:
    st.session_state.state = "idle"

# -------------------------
# UI
# -------------------------
cls = "core " + st.session_state.state
st.markdown(f'<div class="{cls}"></div>', unsafe_allow_html=True)
st.markdown(f"<div class='status'>{st.session_state.state.upper()}</div>",
            unsafe_allow_html=True)

# -------------------------
# AUTO FSM
# -------------------------
if st.session_state.state == "idle":
    if voice_available():
        st.session_state.state = "listening"
        st.rerun()
    time.sleep(0.5)
    st.rerun()

elif st.session_state.state == "listening":
    audio = record_until_silence()
    if audio is None:
        st.session_state.state = "idle"
        st.rerun()

    st.session_state.audio = audio
    st.session_state.state = "thinking"
    st.rerun()

elif st.session_state.state == "thinking":
    text = transcribe(st.session_state.audio)
    if not text:
        st.session_state.state = "idle"
        st.rerun()

    st.session_state.reply = ask(text)
    st.session_state.state = "speaking"
    st.rerun()

elif st.session_state.state == "speaking":
    speak(st.session_state.reply)
    time.sleep(0.3)
    st.session_state.state = "idle"
    st.rerun()
