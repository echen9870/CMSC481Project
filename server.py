from collections import defaultdict
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

#Active users logging in, this prevents multiple clients from authenticating as the same identifier at the same time
activeUsers = set()

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


#taskList is a nested dictionary where the username is the first key and the taskID is the second key
#taskList: {username : {taskID : value}}
taskList = defaultdict(dict)

#taskID is a dictionary which tells the application what taskID the newest task should be when it is created
taskID = defaultdict(int)

#Actual application running
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
            message = interpret_message(message)
            #Sends the response
            send_response(message)

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
    userTaskList = taskList[user]
    if message:
        header, body = message.split(';')
        #Create Command
        if header == "Create":
            #Gets an available taskID and increments taskID[user]
            newTaskId = taskID[user]
            taskID[user] += 1
            #Appends the new task to the userTaskList
            userTaskList[newTaskId] = body
        #Read Command
        if "Read" in header:
            if header[-2:] == "-1":
                return str(userTaskList)
            elif int(header[-1]) not in userTaskList:
                return f"There is not task with ID {header[-1]}"
            else:
                return str(userTaskList[int(header[-1])])
        if "Update" in header:
            if int(header[-1]) not in userTaskList:
                return f"There is not task with ID {header[-1]}"
            else:
                userTaskList[int(header[-1])] = body
                return "Task has been updated"
        if "Delete" in header:
            if int(header[-2:] == "-1"):
                userTaskList.clear()
                return "All tasks have been deleted"
            elif int(header[-1]) not in userTaskList:
                return f"There is not task with ID {header[-1]}"
            else:
                del userTaskList[int(header[-1])]
                return "Task has been deleted"

    return "Received"

#Generates a response for the server to send back to the client
def send_response(message):
    try:
        conn.sendall(message.encode())
    except Exception as e:
        conn.sendall("Error Occured".encode())
        print("Error sending response:", e)

#Actively listens for incoming connection
while True:
  
    #Connection has been received
    conn, addr = sock.accept()
    print('Connected: ',addr)
    
    #Receives username from client
    user = conn.recv(1024).decode()

    #TODO NEED TO CHECK IF THERE IS ALREADY AN EXISTING CONNECTION WITH USER OR IF USERNAME IS VALID

    #Sends the challenge token string
    token = generateChallenge()
    conn.sendall(token.encode())

    #Receives hash from client
    res = conn.recv(1024).decode()

    #Validate authentication
    if user in credentials:
        
        if user in activeUsers:
            conn.sendall(b'400 User already has an active session')

        password = credentials[user]
        hash_input = token + password
        expected_hash = hashlib.md5(hash_input.encode()).hexdigest()

        if res == expected_hash:
            conn.sendall(b'200 SUCCESS')
            application()
            print("Connection Terminated")

        else:
            conn.sendall(b'400 Incorrect Password')
    else:
        conn.sendall(b'400 Invalid User')
    

    

