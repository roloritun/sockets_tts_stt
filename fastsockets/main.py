from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import asyncio
import speech_recognition as sr
from gtts import gTTS
import os
from io import BytesIO

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/tts")
async def tts_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Convert text to speech
            tts = gTTS(text=data, lang="en")
            output = BytesIO()
            tts.write_to_fp(output)
            output.seek(0)
            # Send the audio back to the client
            await websocket.send_bytes(output.read())
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/ws/stt")
async def stt_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    recognizer = sr.Recognizer()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            audio = sr.AudioFile(BytesIO(audio_data))
            with audio as source:
                audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                await websocket.send_text(text)
            except sr.UnknownValueError:
                await websocket.send_text("Could not understand audio")
            except sr.RequestError:
                await websocket.send_text("Error with the speech recognition service")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
async def root():
    return {"message": "WebSocket TTS/STT server running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
