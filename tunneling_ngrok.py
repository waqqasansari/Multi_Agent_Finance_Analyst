import os
import time
from pyngrok import ngrok
import subprocess
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Terminate any existing ngrok tunnels
ngrok.kill()

# Change the current working directory to where run_local.py is located
original_dir = os.getcwd()
os.chdir('multiagent-fin')

# Run the run_local.py script in the background
print("Starting services...")
process = subprocess.Popen(["python", "run_local.py"])

# Give services a moment to start
time.sleep(10)

# Get ngrok authtoken from Colab secrets if available
NGROK_AUTHTOKEN = os.getenv("NGROK_AUTHTOKEN")
print(NGROK_AUTHTOKEN)
if NGROK_AUTHTOKEN:
    ngrok.set_auth_token(NGROK_AUTHTOKEN)
else:
    print("NGROK_AUTHTOKEN not found in Colab secrets. Ngrok might be rate-limited.")

# Open tunnels for each service port (assuming ports 8000, 8001, 8002)
try:
    agent_service_public_url = ngrok.connect(8000)
    stt_service_public_url = ngrok.connect(8001)
    tts_service_public_url = ngrok.connect(8002)

    print(f"Agent Service Public URL: {agent_service_public_url}")
    print(f"STT Service Public URL: {stt_service_public_url}")
    print(f"TTS Service Public URL: {tts_service_public_url}")

    print("\nAPI services are now accessible via the public URLs.")
    print("Keep this cell running to keep the tunnels active.")

    # Keep the cell alive to maintain the tunnels
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Tunnels stopped.")
    finally:
        # Clean up ngrok tunnels and the background process
        ngrok.kill()
        process.terminate()
        os.chdir(original_dir) # Change back to original directory
except Exception as e:
    print(f"An error occurred: {e}")
    # Ensure process is terminated and directory is changed back in case of error
    process.terminate()
    os.chdir(original_dir)