import pyttsx3
import speech_recognition as sr
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Function to perform TTS
def text_to_speech(text: str):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to perform STT
def speech_to_text(audio_data: bytes):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "STT service error"

@app.websocket("/ws/tts")
async def websocket_tts(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            text = await websocket.receive_text()
            text_to_speech(text)
            await websocket.send_text(f"TTS Completed: {text}")
    except WebSocketDisconnect:
        print("TTS WebSocket disconnected")

@app.websocket("/ws/stt")
async def websocket_stt(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            recognized_text = speech_to_text(audio_data)
            await websocket.send_text(recognized_text)
    except WebSocketDisconnect:
        print("STT WebSocket disconnected")

# Sample HTML to test the WebSockets
@app.get("/")
def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket TTS & STT</title>
    </head>
    <body>
        <h2>Text-to-Speech (TTS) WebSocket</h2>
        <input id="ttsInput" type="text" placeholder="Enter text">
        <button onclick="sendTTS()">Send TTS</button>
        <p id="ttsResponse"></p>
        
        <h2>Speech-to-Text (STT) WebSocket</h2>
        <button onclick="startSTT()">Start Recording</button>
        <p id="sttResponse"></p>
        
        <script>
            const ttsSocket = new WebSocket("ws://localhost:8000/ws/tts");
            const sttSocket = new WebSocket("ws://localhost:8000/ws/stt");

            ttsSocket.onmessage = function(event) {
                document.getElementById("ttsResponse").innerText = event.data;
            };

            sttSocket.onmessage = function(event) {
                document.getElementById("sttResponse").innerText = event.data;
            };

            function sendTTS() {
                const text = document.getElementById("ttsInput").value;
                ttsSocket.send(text);
            }

            async function startSTT() {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                mediaRecorder.ondataavailable = async function(event) {
                    const reader = new FileReader();
                    reader.readAsArrayBuffer(event.data);
                    reader.onloadend = function() {
                        sttSocket.send(reader.result);
                    };
                };

                setTimeout(() => {
                    mediaRecorder.stop();
                }, 15000); // Record for 5 seconds
            }
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
