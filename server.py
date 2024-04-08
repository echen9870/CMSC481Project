from collections import defaultdict
import hashlib
import random
import socket
import signal
import sys
import select

#Valid credentials
credentials = {
    "echen9" : "password1",
    "peterj1" : "password2"
}

#Active users logging in, this prevents multiple clients from authenticating as the same identifier at the same time
activeUsers = set()
connections = {}

#Creates our server address
srvr_addr = ("0.0.0.0", 12345)

#Sets up our socket and binds it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(srvr_addr)
sock.listen(1)
print("Server is setup")

#Creates epoll instnace
epoll = select.epoll()

# Register server socket to epoll
epoll.register(sock.fileno(), select.EPOLLIN)

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
def application(message):
    if message == "Exit":
        print("Terminating connection")
        conn.close()
        activeUsers.remove(user)
    else:
        #Gets the message and checks if client has terminated it
        message = interpret_message(message)

        #Sends the response
        return send_response(message)

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

    #Get events
    events = epoll.poll(2)
    #Iterate through each event
    for fileno, event in events:
        #Accepting new connections
        if fileno == sock.fileno():

            #Connection has been received
            conn, addr = sock.accept()
            print("Connected to:", addr)
            #Authenticating connection
            user = conn.recv(1024).decode()
            token = generateChallenge()
            conn.sendall(token.encode())
            res = conn.recv(1024).decode()

            if user in credentials:
                if user in activeUsers:
                    conn.sendall(b'400 User already has an active session')
                    conn.close()
                else:
                    password = credentials[user]
                    hash_input = token + password
                    expected_hash = hashlib.md5(hash_input.encode()).hexdigest()

                    if res == expected_hash:
                        # Register connection and adds user to activeUser
                        epoll.register(conn.fileno(), select.EPOLLIN)
                        connections[conn.fileno()] = conn
                        activeUsers.add(user)
                        conn.sendall(b'200 SUCCESS')
                    else:
                        conn.sendall(b'400 Incorrect Password')
                        conn.close()
            else:
                conn.sendall(b'400 Invalid User')
                conn.close()

        #Handling incoming data from existing connection
        elif event & select.EPOLLIN:
            conn = connections[fileno]
            data = conn.recv(1024).decode()
            if not data:
                # If no data received, close the connection
                epoll.unregister(fileno)
                conn.close()
                del connections[fileno]
            else:
                response = application(data)
                conn.sendall(response)
    


