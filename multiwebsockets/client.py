import socket
import pyaudio

def play_audio(audio_data):
    audio = pyaudio.PyAudio()
    
    # Open a stream to play the received audio data
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
    stream.write(audio_data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5000

client_socket.connect((host, port))

# Text to send to the server
#text = "Hello! This is a test message with enhanced features."

text  = "The Sun enters grounded Virgo on Thursday, signaling a focus on organization, attention to detail, and practical problem-solving. The Taurus Moon is in harmony with the Virgo Sun on Friday - " \
        "expect a harmonious flow of energy between your emotions and your sense of self, leading to increased confidence and inner balance. Mercury connects to Mars on Saturday, bringing sharp mental "\
        "clarity and quick decision-making abilities,  making it an ideal time for tackling tasks that require focus and precision. The Taurus Moon is in harmony with Uranus on Sunday - "\
        "embrace the changes by staying open-minded and flexible, allowing yourself to explore new perspectives or opportunities that arise."

client_socket.sendall(text.encode('utf-8'))

# Receive the streamed audio from the server
audio_data = b''
while True:
    packet = client_socket.recv(4096)
    if not packet:
        break
    audio_data += packet

# Play the received audio
play_audio(audio_data)

# Close the connection
client_socket.close()
