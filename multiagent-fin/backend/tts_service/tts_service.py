from fastapi import FastAPI, Response
from openai import OpenAI
from pydantic import BaseModel
import io
import os

app = FastAPI(title="Text-to-Speech Service")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TTSRequest(BaseModel):
    text: str

@app.post("/synthesize")
async def synthesize_speech(request: TTSRequest):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=request.text
        )
        return Response(content=response.content, media_type="audio/mp3")
    except Exception as e:
        return {"error": str(e)}