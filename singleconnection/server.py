import socket
import pyttsx3
import pyaudio

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

# Set up socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5000
server_socket.bind((host, port))
server_socket.listen(1)

print("Server listening on port", port)

def speak_text(text):
    engine.say(text)
    engine.save_to_file(text, 'test.mp3')
    engine.runAndWait()

def stream_audio(audio_data):
    # Setup PyAudio stream for audio output
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
    
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    audio.terminate()

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    
    # Receive the text from the client
    text = client_socket.recv(1024).decode('utf-8')
    print(f"Received text: {text}")
    
    # Convert text to speech and stream it
    if text:
        speak_text(text)
        
    client_socket.close()
