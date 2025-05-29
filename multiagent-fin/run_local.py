import os
import subprocess
import threading
import time
import webbrowser
from dotenv import load_dotenv

load_dotenv()

def run_service(service_name, port):
    command = f"uvicorn backend.{service_name}.{service_name}:app --reload --port {port}"
    print(command)
    subprocess.run(command, shell=True)

def run_streamlit():
    subprocess.run("streamlit run ../streamlit-app/app.py", shell=True)

if __name__ == "__main__":
    # Start services in background threads
    threading.Thread(target=run_service, args=("agent_service", 8000), daemon=True).start()
    threading.Thread(target=run_service, args=("stt_service", 8001), daemon=True).start()
    threading.Thread(target=run_service, args=("tts_service", 8002), daemon=True).start()
    
    # # Give services time to start
    # time.sleep(5)
    
    # # Start Streamlit and open browser
    # threading.Thread(target=run_streamlit, daemon=True).start()
    # time.sleep(3)
    # webbrowser.open("http://localhost:8501")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down services...")