import socket
import hashlib

# Server address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 12345

# Keyword to identify the client
KEYWORD = "IDENTITY"

# Predefined user credentials
username = "user"
password = "password"

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    # Send the keyword to identify the client
    client_socket.sendall(f"{KEYWORD}: {username}".encode())

    # Receive the challenge token from the server
    challenge_token = client_socket.recv(1024).decode().strip()

    # Generate the response by appending the password to the challenge token and calculating the MD5 hash
    response = hashlib.md5((challenge_token + password).encode()).hexdigest()

    # Send the response to the server
    client_socket.sendall(response.encode())

    # Receive the authentication result from the server
    auth_result = client_socket.recv(1024).decode().strip()

    # Display the authentication result
    if auth_result == '200':
        print("Authentication successful")
    else:
        print("Authentication failed")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the socket
    client_socket.close()
