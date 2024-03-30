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

ip_addr = "0.0.0.0"
port = 12345

#Creates our server address
srvr_addr = (ip_addr, port)

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

#Actively listens for incoming connection
while True:
  
    #Connection has been received
    conn, addr = sock.accept()
    print('Connected: ',addr)
    
    #Receives username from client
    user = conn.recv(1024).decode()

    #Sends the challenge token string
    token = generateChallenge()
    print("Token: ", token)
    conn.sendall(token.encode())

    #Receives hash from client
    
    res = conn.recv(1024).decode()
    print("User: ", user)
    print("Hash From Client:", res)

    #Validate authentication
    if user in credentials:
        password = credentials[user]
        hash_input = token + password
        print("Input to be hashed:", hash_input)
        expected_hash = hashlib.md5(hash_input.encode()).hexdigest()
        print("Expected hash: ", expected_hash)
        if res == expected_hash:
            conn.sendall(b'200 SUCCESS')
        else:
            conn.sendall(b'400 FAIL')
    else:
        conn.sendall(b'400 FAIL')

    #Close connection
    conn.close()

    

