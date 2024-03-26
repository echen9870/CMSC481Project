import random
import socket
import time
import argparse

parser = argparse.ArgumentParser(description="Simple Server for N/w Delays")
parser.add_argument('-s', '--server', type=str, default="0.0.0.0")
parser.add_argument('-p', '--port', type=int, default=32768)
parser.add_argument('-b', '--buffer',  type=int, default=10)
parser.add_argument('-d', '--delay',  type=int, default=0)
args = parser.parse_args()

ip_addr = args.server
port = args.port
buffer = args.buffer
delay = args.delay

#Creates our server address
srvr_addr = (ip_addr, port)

#Sets up our socket and binds it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(srvr_addr)
sock.listen(1)

#Generates the challenge string needed for authentication
def generateChallenge():
    res = "".join([chr(random.randint(ord('a'), ord('z'))) for i in range(10)])
    return res

#Actively listens for incoming connection
while True:
  
    #Connection has been received
    data, addr = sock.accept()
    print('Connected: ',addr)
  
    #Sends the challenge tocket string
    token = generateChallenge()
    print("Token: ", token)
    if data:
        print("Server receiving: ", data.decode())
        response = ("%s"%(data.decode())).lower()
        print("Server sending: ", response)
        sent = sock.sendto(response.encode(), addr)
        time.sleep(delay)

