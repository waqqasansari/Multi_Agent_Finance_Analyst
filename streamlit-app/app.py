import streamlit as st
import requests
import time
from streamlit.components.v1 import html

st.set_page_config(page_title="Finance Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>💬 Finance Chatbot Assistant</h1>", unsafe_allow_html=True)

# 🔁 Updated with your current ngrok URLs
AGENT_API_URL = "https://c519-34-71-203-237.ngrok-free.app"
STT_API_URL = "https://2a55-34-71-203-237.ngrok-free.app"
TTS_API_URL = "https://da58-34-71-203-237.ngrok-free.app"

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
                "session_id": st.session_state.session_id,
                "previous_response_id": st.session_state.prev_response_id
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











# # File: streamlit_app/app.py
# import streamlit as st
# import requests
# import time

# st.set_page_config(page_title="Finance Chatbot", layout="centered")
# st.title("💬 Finance Chatbot Assistant")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.prev_response_id = None
#     st.session_state.session_id = f"session_{int(time.time())}"

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])
#         if msg["role"] == "assistant" and msg.get("audio"):
#             st.audio(msg["audio"], format="audio/mp3")

# # Audio input
# audio_bytes = st.audio_input("🎙️ Speak your query", key=f"audio_{st.session_state.session_id}")

# if audio_bytes is not None:
#     # Transcribe audio
#     with st.spinner("Transcribing..."):
#         stt_resp = requests.post(
#             "http://localhost:8001/transcribe",
#             files={"audio": ("query.wav", audio_bytes.getvalue(), "audio/wav")},
#             timeout=30
#         )
    
#     if stt_resp.status_code != 200:
#         st.error("Speech recognition failed")
#         st.stop()
    
#     user_text = stt_resp.json().get("text", "").strip()
    
#     # Add to chat history
#     st.session_state.messages.append({"role": "user", "content": user_text})
#     st.chat_message("user").markdown(user_text)
    
#     # Process query
#     with st.spinner("Analyzing..."):
#         orch_resp = requests.post(
#             "http://localhost:8000/query",
#             json={
#                 "query": user_text,
#                 "session_id": st.session_state.session_id,
#                 "previous_response_id": st.session_state.prev_response_id
#             },
#             timeout=120
#         )
    
#     if orch_resp.status_code != 200:
#         st.error("Analysis failed")
#         st.stop()
    
#     response_data = orch_resp.json()
#     answer_text = response_data.get("text", "")
#     st.session_state.prev_response_id = response_data.get("response_id")
    
#     # Generate speech
#     with st.spinner("Generating voice..."):
#         tts_resp = requests.post(
#             "http://localhost:8002/synthesize",
#             json={"text": answer_text},
#             timeout=60
#         )
    
#     audio_data = tts_resp.content if tts_resp.status_code == 200 else None
    
#     # Display response
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer_text,
#         "audio": audio_data
#     })
    
#     with st.chat_message("assistant"):
#         st.markdown(answer_text)
#         if audio_data:
#             st.audio(audio_data, format="audio/mp3")

# # Reset button
# if st.button("New Conversation"):
#     st.session_state.messages = []
#     st.session_state.prev_response_id = None
#     st.session_state.session_id = f"session_{int(time.time())}"
#     requests.post("http://agent_service:8000/reset")
#     st.experimental_rerun()

# # File: streamlit_app/app.py
# import streamlit as st
# import requests
# import time
# import json
# import logging
# from typing import Optional
# import traceback
# from datetime import datetime

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Configuration
# CONFIG = {
#     "STT_SERVICE_URL": "http://localhost:8001",
#     "ORCHESTRATOR_URL": "http://localhost:8000", 
#     "TTS_SERVICE_URL": "http://localhost:8002",
#     "TIMEOUTS": {
#         "transcribe": 30,
#         "query": 120,
#         "synthesize": 60,
#         "reset": 10
#     },
#     "MAX_RETRIES": 3,
#     "RETRY_DELAY": 1
# }

# st.set_page_config(
#     page_title="Finance multiagent Chatbot", 
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# def check_service_health(service_name: str, url: str) -> bool:
#     """Check if a service is available"""
#     try:
#         response = requests.get(f"{url}/health", timeout=5)
#         return response.status_code == 200
#     except:
#         return False

# def make_request_with_retry(func, max_retries: int = 3, delay: float = 1):
#     """Make HTTP request with retry logic"""
#     for attempt in range(max_retries):
#         try:
#             return func()
#         except requests.exceptions.RequestException as e:
#             if attempt == max_retries - 1:
#                 raise e
#             logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
#             time.sleep(delay * (attempt + 1))  # Exponential backoff
    
# def safe_transcribe_audio(audio_bytes) -> Optional[str]:
#     """Safely transcribe audio with error handling"""
#     try:
#         def transcribe_request():
#             return requests.post(
#                 f"{CONFIG['STT_SERVICE_URL']}/transcribe",
#                 files={"audio": ("query.wav", audio_bytes, "audio/wav")},
#                 timeout=CONFIG['TIMEOUTS']['transcribe']
#             )
        
#         response = make_request_with_retry(transcribe_request, CONFIG['MAX_RETRIES'])
        
#         if response.status_code == 200:
#             result = response.json()
#             text = result.get("text", "").strip()
#             if not text:
#                 st.error("🎙️ No speech detected in audio")
#                 return None
#             return text
#         else:
#             error_msg = f"Transcription failed (Status: {response.status_code})"
#             try:
#                 error_detail = response.json().get("error", "Unknown error")
#                 error_msg += f": {error_detail}"
#             except:
#                 error_msg += f": {response.text[:200]}"
#             st.error(f"🎙️ {error_msg}")
#             return None
            
#     except requests.exceptions.Timeout:
#         st.error("🎙️ Speech recognition timed out. Please try with a shorter audio clip.")
#         return None
#     except requests.exceptions.ConnectionError:
#         st.error("🎙️ Cannot connect to speech recognition service. Please check if it's running.")
#         return None
#     except Exception as e:
#         logger.error(f"Transcription error: {e}")
#         st.error(f"🎙️ Speech recognition failed: {str(e)}")
#         return None

# def safe_process_query(query: str, session_id: str, prev_response_id: Optional[str]) -> Optional[dict]:
#     """Safely process query with error handling"""
#     try:
#         def query_request():
#             return requests.post(
#                 f"{CONFIG['ORCHESTRATOR_URL']}/query",
#                 json={
#                     "query": query,
#                     "session_id": session_id,
#                     "previous_response_id": prev_response_id
#                 },
#                 timeout=CONFIG['TIMEOUTS']['query']
#             )
        
#         response = make_request_with_retry(query_request, CONFIG['MAX_RETRIES'])
        
#         if response.status_code == 200:
#             return response.json()
#         else:
#             error_msg = f"Query processing failed (Status: {response.status_code})"
#             try:
#                 error_detail = response.json().get("error", "Unknown error")
#                 error_msg += f": {error_detail}"
#             except:
#                 error_msg += f": {response.text[:200]}"
#             st.error(f"🤖 {error_msg}")
#             return None
            
#     except requests.exceptions.Timeout:
#         st.error("🤖 Analysis timed out. The query might be too complex. Please try a simpler question.")
#         return None
#     except requests.exceptions.ConnectionError:
#         st.error("🤖 Cannot connect to analysis service. Please check if it's running.")
#         return None
#     except Exception as e:
#         logger.error(f"Query processing error: {e}")
#         st.error(f"🤖 Analysis failed: {str(e)}")
#         return None

# def safe_synthesize_speech(text: str) -> Optional[bytes]:
#     """Safely synthesize speech with error handling"""
#     try:
#         def tts_request():
#             return requests.post(
#                 f"{CONFIG['TTS_SERVICE_URL']}/synthesize",
#                 json={"text": text},
#                 timeout=CONFIG['TIMEOUTS']['synthesize']
#             )
        
#         response = make_request_with_retry(tts_request, CONFIG['MAX_RETRIES'])
        
#         if response.status_code == 200:
#             return response.content
#         else:
#             logger.warning(f"TTS failed (Status: {response.status_code})")
#             return None
            
#     except requests.exceptions.Timeout:
#         logger.warning("TTS request timed out")
#         return None
#     except requests.exceptions.ConnectionError:
#         logger.warning("Cannot connect to TTS service")
#         return None
#     except Exception as e:
#         logger.error(f"TTS error: {e}")
#         return None

# def reset_conversation():
#     """Reset conversation state"""
#     try:
#         requests.post(
#             f"{CONFIG['ORCHESTRATOR_URL']}/reset",
#             timeout=CONFIG['TIMEOUTS']['reset']
#         )
#     except Exception as e:
#         logger.warning(f"Reset request failed: {e}")
#         # Continue anyway since local state will be reset
    
#     st.session_state.messages = []
#     st.session_state.prev_response_id = None
#     st.session_state.session_id = f"session_{int(time.time())}"
#     st.success("🔄 Conversation reset successfully!")

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     st.session_state.prev_response_id = None
#     st.session_state.session_id = f"session_{int(time.time())}"
#     st.session_state.service_status_checked = False

# # Sidebar with service status and controls
# with st.sidebar:
#     st.header("🔧 System Status")
    
#     if st.button("🔄 Check Services") or not st.session_state.service_status_checked:
#         st.session_state.service_status_checked = True
        
#         services = [
#             ("Speech Recognition", CONFIG['STT_SERVICE_URL']),
#             ("AI Assistant", CONFIG['ORCHESTRATOR_URL']),
#             ("Text-to-Speech", CONFIG['TTS_SERVICE_URL'])
#         ]
        
#         for service_name, url in services:
#             if check_service_health(service_name, url):
#                 st.success(f"✅ {service_name}")
#             else:
#                 st.error(f"❌ {service_name}")
    
#     st.divider()
    
#     st.header("⚙️ Settings")
    
#     # Audio settings
#     st.subheader("🎙️ Audio")
#     enable_tts = st.checkbox("Enable voice responses", value=True)
    
#     # Session info
#     st.subheader("📊 Session Info")
#     st.text(f"Session: {st.session_state.session_id}")
#     st.text(f"Messages: {len(st.session_state.messages)}")
    
#     # Reset button
#     if st.button("🗑️ New Conversation", type="primary"):
#         reset_conversation()
#         st.rerun()

# # Main interface
# st.title("💬 Finance Chatbot Assistant")
# st.markdown("*Ask me anything about finance, investments, or market analysis!*")

# # Display chat history
# chat_container = st.container()
# with chat_container:
#     for i, msg in enumerate(st.session_state.messages):
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])
            
#             # Display audio for assistant messages if available
#             if msg["role"] == "assistant" and msg.get("audio") and enable_tts:
#                 st.audio(msg["audio"], format="audio/mp3")
            
#             # Add timestamp for debugging
#             if st.session_state.get("debug_mode", False):
#                 st.caption(f"Message {i} • {msg.get('timestamp', 'Unknown time')}")

# # Text input
# text_input = st.chat_input("💬 Type your message here...")

# # Audio input
# st.markdown("---")
# col1, col2 = st.columns([3, 1])

# with col1:
#     audio_bytes = st.audio_input("🎙️ Or speak your query", key=f"audio_{st.session_state.session_id}")

# with col2:
#     st.markdown("<br>", unsafe_allow_html=True)  # Spacing
#     debug_mode = st.checkbox("🐛 Debug", value=False)
#     st.session_state.debug_mode = debug_mode

# # Process text input
# if text_input:
#     user_text = text_input.strip()
    
#     # Add user message to chat
#     timestamp = datetime.now().isoformat()
#     st.session_state.messages.append({
#         "role": "user", 
#         "content": user_text,
#         "timestamp": timestamp
#     })
    
#     with st.chat_message("user"):
#         st.markdown(user_text)
    
#     # Process the query
#     with st.spinner("🤖 Analyzing your question..."):
#         response_data = safe_process_query(
#             user_text, 
#             st.session_state.session_id, 
#             st.session_state.prev_response_id
#         )
    
#     if response_data:
#         answer_text = response_data.get("text", "I'm sorry, I couldn't generate a response.")
#         st.session_state.prev_response_id = response_data.get("response_id")
        
#         # Generate speech if enabled
#         audio_data = None
#         if enable_tts and answer_text:
#             with st.spinner("🔊 Generating voice response..."):
#                 audio_data = safe_synthesize_speech(answer_text)
        
#         # Add assistant message to chat
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": answer_text,
#             "audio": audio_data,
#             "timestamp": datetime.now().isoformat()
#         })
        
#         # Display response
#         with st.chat_message("assistant"):
#             st.markdown(answer_text)
#             if audio_data and enable_tts:
#                 st.audio(audio_data, format="audio/mp3")
    
#     st.rerun()

# # Process audio input
# if audio_bytes is not None:
#     # Transcribe audio
#     with st.spinner("🎙️ Converting speech to text..."):
#         user_text = safe_transcribe_audio(audio_bytes.getvalue())
    
#     if user_text:
#         # Add user message to chat
#         timestamp = datetime.now().isoformat()
#         st.session_state.messages.append({
#             "role": "user", 
#             "content": user_text,
#             "timestamp": timestamp
#         })
        
#         with st.chat_message("user"):
#             st.markdown(user_text)
        
#         # Process the query
#         with st.spinner("🤖 Analyzing your question..."):
#             response_data = safe_process_query(
#                 user_text, 
#                 st.session_state.session_id, 
#                 st.session_state.prev_response_id
#             )
        
#         if response_data:
#             answer_text = response_data.get("text", "I'm sorry, I couldn't generate a response.")
#             st.session_state.prev_response_id = response_data.get("response_id")
            
#             # Generate speech if enabled
#             audio_data = None
#             if enable_tts and answer_text:
#                 with st.spinner("🔊 Generating voice response..."):
#                     audio_data = safe_synthesize_speech(answer_text)
            
#             # Add assistant message to chat
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": answer_text,
#                 "audio": audio_data,
#                 "timestamp": datetime.now().isoformat()
#             })
            
#             # Display response
#             with st.chat_message("assistant"):
#                 st.markdown(answer_text)
#                 if audio_data and enable_tts:
#                     st.audio(audio_data, format="audio/mp3")
        
#         st.rerun()

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: gray; font-size: small;'>"
#     "💡 Tip: You can either type your message or use voice input above"
#     "</div>", 
#     unsafe_allow_html=True
# )