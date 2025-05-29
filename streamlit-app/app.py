import streamlit as st
import requests
import time
from streamlit.components.v1 import html

st.set_page_config(page_title="Finance Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>💬 Finance Chatbot Assistant</h1>", unsafe_allow_html=True)

# 🔁 Updated with your current ngrok URLs
AGENT_API_URL = "https://76f6-2405-201-604f-a04d-286b-f699-50b4-a5f5.ngrok-free.app"
STT_API_URL = "https://dc37-2405-201-604f-a04d-286b-f699-50b4-a5f5.ngrok-free.app"
TTS_API_URL = "https://7cc7-2405-201-604f-a04d-286b-f699-50b4-a5f5.ngrok-free.app"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.prev_response_id = None
    st.session_state.session_id = f"session_{int(time.time())}"

# Chat container with visual distinction
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role_color = "#DCF8C6" if msg["role"] == "user" else "#F1F0F0"
        align = "flex-end" if msg["role"] == "user" else "flex-start"
        st.markdown(f"""
            <div style='display: flex; justify-content: {align}; margin-bottom: 10px;'>
                <div style='background-color: {role_color}; padding: 10px 15px; border-radius: 10px; max-width: 80%;'>
                    {msg["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)
        if msg["role"] == "assistant" and msg.get("audio"):
            st.audio(msg["audio"], format="audio/mp3")

st.markdown("---")
st.markdown("🎙️ **Record your question below:**")

# Audio input
audio_bytes = st.audio_input(" ", key=f"audio_{st.session_state.session_id}")

if audio_bytes is not None:
    # Step 1: Transcribe audio
    with st.status("Transcribing audio...", expanded=False):
        stt_resp = requests.post(
            f"{STT_API_URL}/transcribe",
            files={"audio": ("query.wav", audio_bytes.getvalue(), "audio/wav")},
            timeout=30
        )

    if stt_resp.status_code != 200:
        st.error("❌ Speech recognition failed.")
        st.stop()

    user_text = stt_resp.json().get("text", "").strip()
    st.session_state.messages.append({"role": "user", "content": user_text})
    with chat_container:
        st.markdown(f"""
            <div style='display: flex; justify-content: flex-end; margin-bottom: 10px;'>
                <div style='background-color: #DCF8C6; padding: 10px 15px; border-radius: 10px; max-width: 80%;'>
                    {user_text}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Step 2: Analyze text
    with st.status("Analyzing query with agent...", expanded=False):
        orch_resp = requests.post(
            f"{AGENT_API_URL}/query",
            json={
                "query": user_text,
                "session_id": st.session_state.session_id
            },
            timeout=120
        )

    if orch_resp.status_code != 200:
        st.error("❌ Analysis failed.")
        st.stop()

    response_data = orch_resp.json()
    answer_text = response_data.get("text", "")
    st.session_state.prev_response_id = response_data.get("response_id")

    # Step 3: Generate voice
    with st.status("Generating voice response...", expanded=False):
        tts_resp = requests.post(
            f"{TTS_API_URL}/synthesize",
            json={"text": answer_text},
            timeout=60
        )

    audio_data = tts_resp.content if tts_resp.status_code == 200 else None

    # Display assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer_text,
        "audio": audio_data
    })

    with chat_container:
        st.markdown(f"""
            <div style='display: flex; justify-content: flex-start; margin-bottom: 10px;'>
                <div style='background-color: #F1F0F0; padding: 10px 15px; border-radius: 10px; max-width: 80%;'>
                    {answer_text}
                </div>
            </div>
        """, unsafe_allow_html=True)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")

# Reset conversation
st.markdown("---")
col1, col2, _ = st.columns([1, 1, 2])
with col1:
    if st.button("🔄 New Conversation"):
        st.session_state.messages = []
        st.session_state.prev_response_id = None
        st.session_state.session_id = f"session_{int(time.time())}"
        requests.post("http://localhost:8000/reset")
        st.experimental_rerun()