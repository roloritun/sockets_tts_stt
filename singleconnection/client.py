import socket

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5001

client_socket.connect((host, port))

# Text to send to the server
#text = "Hello! This is a test message."
text = "The Sun enters grounded Virgo on Thursday, signaling a focus on organization, attention to detail, and practical problem-solving. The Taurus Moon is in harmony with the Virgo Sun on Friday - " \
        "expect a harmonious flow of energy between your emotions and your sense of self, leading to increased confidence and inner balance. Mercury connects to Mars on Saturday, bringing sharp mental "\
        "clarity and quick decision-making abilities,  making it an ideal time for tackling tasks that require focus and precision. The Taurus Moon is in harmony with Uranus on Sunday - "\
        "embrace the changes by staying open-minded and flexible, allowing yourself to explore new perspectives or opportunities that arise."

client_socket.sendall(text.encode('utf-8'))

# Close the connection
client_socket.close()
