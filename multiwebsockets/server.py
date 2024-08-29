import socket
import threading
import pyttsx3
import io
import wave

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Set up socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5000
server_socket.bind((host, port))
server_socket.listen(5)

print("Server listening on port", port)

def handle_client(client_socket, addr):
    print(f"Connection from {addr}")
    
    # Receive the text from the client
    text = client_socket.recv(1024).decode('utf-8')
    print(f"Received text: {text}")
    
    # Convert text to speech and capture the audio data
    if text:
        audio_data = convert_text_to_speech(text)
        
        # Stream the audio data back to the client
        client_socket.sendall(audio_data)
        
    client_socket.close()

def convert_text_to_speech(text):
    output = io.BytesIO()  # In-memory buffer to store audio
    engine.save_to_file(text, 'output.wav')  # Save the TTS output as a WAV file
    engine.runAndWait()
    
    # Load the saved WAV file and convert it to bytes
    with open('output.wav', 'rb') as f:
        audio_data = f.read()
    
    return audio_data

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
