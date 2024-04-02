import hashlib
import random
import socket
import signal
import sys

#Valid credentials
credentials = {
    "echen9" : "password1",
    "peterj1" : "password2"
}

#Creates our server address
srvr_addr = ("0.0.0.0", 12345)

#Sets up our socket and binds it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(srvr_addr)
sock.listen(1)
print("Server is setup")

#Generates the challenge string needed for authentication
def generateChallenge():
    res = "".join([chr(random.randint(ord('a'), ord('z'))) for i in range(10)])
    return res

# Signal handler to catch Ctrl+C and close the server 
def signal_handler(sig, frame):
    print("Closing server...")
    sock.close()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

def application():
    while(True):
        #Gets the message
        message = accept_message()
        if message == "Exit":
            print("Terminating connection")
            conn.close()
            break
        else:
            #Gets the message and checks if client has terminated it
            terminated = interpret_message(message)

            #Sends the response
            send_response("Received")

#Accepts the message from the client, only decodes and returns the message
def accept_message():
    try:
        message = conn.recv(1024).decode()
        return message
    except OSError as e:
        print("Error receiving message:", e)
        print("Terminating connection")
        conn.close()
        return None

#Interprets the message, if the message is to Exit, returns True, which allows the connection to be terminated
def interpret_message(message):
    if not message:
        return True
    return False

#Generates a response for the server to send back to the client
def send_response(message):
    try:
        conn.sendall(message.encode())
    except Exception as e:
        print("Error sending response:", e)

#Actively listens for incoming connection
while True:
  
    #Connection has been received
    conn, addr = sock.accept()
    print('Connected: ',addr)
    
    #Receives username from client
    user = conn.recv(1024).decode()

    #Sends the challenge token string
    token = generateChallenge()
    conn.sendall(token.encode())

    #Receives hash from client
    res = conn.recv(1024).decode()

    #Validate authentication
    if user in credentials:

        password = credentials[user]
        hash_input = token + password
        expected_hash = hashlib.md5(hash_input.encode()).hexdigest()

        if res == expected_hash:
            conn.sendall(b'200 SUCCESS')
            application()
            print("Connection Terminated")

        else:
            conn.sendall(b'400 FAIL')
    else:
        conn.sendall(b'400 FAIL')
    

    

