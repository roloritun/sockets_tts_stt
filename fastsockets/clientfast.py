import websockets
import asyncio


async def tts_client():
    uri = "ws://localhost:8000/ws/tts"
    async with websockets.connect(uri) as websocket:
        text = "The Sun enters grounded Virgo on Thursday, signaling a focus on organization, attention to detail, and practical problem-solving. The Taurus Moon is in harmony with the Virgo Sun on Friday - " \
        "expect a harmonious flow of energy between your emotions and your sense of self, leading to increased confidence and inner balance. Mercury connects to Mars on Saturday, bringing sharp mental "\
        "clarity and quick decision-making abilities,  making it an ideal time for tackling tasks that require focus and precision. The Taurus Moon is in harmony with Uranus on Sunday - "\
        "embrace the changes by staying open-minded and flexible, allowing yourself to explore new perspectives or opportunities that arise."
        await websocket.send(text)
        audio_data = await websocket.recv()
        with open("output.mp3", "wb") as f:
            f.write(audio_data)
        print("Received TTS audio saved to output.mp3")


async def stt_client(audio_file_path):
    uri = "ws://localhost:8000/ws/stt"
    async with websockets.connect(uri) as websocket:
        with open(audio_file_path, "rb") as audio_file:
            await websocket.send(audio_file.read())
        response = await websocket.recv()
        print(f"STT Response: {response}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tts_client())
    loop.run_until_complete(stt_client("input_audio.wav"))
