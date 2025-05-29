from fastapi import FastAPI, File, UploadFile
from openai import OpenAI
import io
import os
import tempfile
import traceback

app = FastAPI(title="Speech-to-Text Service")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# @app.post("/transcribe")
# async def transcribe_audio(audio: UploadFile = File(...)): #The ... (ellipsis) indicates that this parameter is required
#     content = await audio.read()
#     try:
#         transcription = client.audio.transcriptions.create(
#             file=io.BytesIO(content),
#             model="whisper-1",
#             response_format="text"
#         )
#         return {"text": transcription}
#     except Exception as e:
#         return {"error": str(e)}
@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    tmp_path = None  # Initialize to None at the start

    try:
        print(f"Received file: {audio.filename}")  # ✅ Log filename

        suffix = os.path.splitext(audio.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await audio.read())
            tmp_path = tmp.name  # This line sets tmp_path
            print(f"Saved temp file to: {tmp_path}")  # ✅ Log temp path

        with open(tmp_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=f,
                model="whisper-1",
                response_format="text"
            )

        return {"text": transcription}
    
    except Exception as e:
        print("⛔ Exception occurred during transcription!")
        traceback.print_exc()  # ✅ Full traceback
        return {"error": f"Exception: {str(e)}"}

    finally:
        # Check if tmp_path was assigned and file exists before cleanup
        if tmp_path is not None and os.path.exists(tmp_path):
            os.remove(tmp_path)
            print(f"🧹 Deleted temp file: {tmp_path}")