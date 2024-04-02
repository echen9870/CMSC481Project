import socket
import hashlib
import time

# Server address and port
SERVER_ADDRESS = '172.21.2.5'
SERVER_PORT = 12345

#Get username/password function can be later implemented so user can type in username/password
def getUsername():
    username = "echen9"
    return username

def getPassword():
    password = "password1"
    return password

#TODO NEED TO IMPLEMENT INPUT CHECKING
def getUserInput():
    #Ask user for command type
    command = input("Enter the type of command you would like to execute (Create, Read, Delete, Update) or type Exit to exit:")
    #Create Command
    if command == "Exit":
        return "Exit"
    elif command == "Create":
        taskName = input("What is the name of the task:")
        return f"{command};{taskName}"
    elif command == "Read":
        taskID = input("What is the task you want to read (Leave -1 to read all tasks):")
        return f"{command} {taskID};"
    elif command == "Delete":
        taskID = input("What is the id of the task to delete (Leave -1 to delete all tasks):")
        return f"{command} {taskID};"
    elif command == "Update":
        taskID = input("What is the id of the task to update:")
        taskName = input("What is the new name of the task:")
        return f"{command} {taskID};{taskName}"



if __name__ == "__main__":

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    authenticated = False

    #Client is trying to authenticate
    while not authenticated:
        try:
            # Connect to the server
            print("Attemptiong to connect to ", SERVER_ADDRESS," ", SERVER_PORT)
            client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

            # Send the username to identify the client
            username = getUsername()
            client_socket.sendall(f"{username}".encode())

            # Receive the challenge token from the server
            challenge_token = client_socket.recv(1024).decode().strip()

            # Generate the response by appending the password to the challenge token and calculating the MD5 hash
            hashMessage = hashlib.md5((challenge_token + getPassword()).encode()).hexdigest()

            # Send the response to the server
            client_socket.sendall(hashMessage.encode())

            # Receive the authentication result from the server
            auth_result = client_socket.recv(1024).decode().strip()

            # Display the authentication result
            if auth_result == '200 SUCCESS':
                print("Authentication successful")
                authenticated = True
                # Loop for sending commands to the server
                while True:
                    message = getUserInput()
                    client_socket.sendall(message.encode())
                    if message == "Exit":
                        break
                    response = client_socket.recv(1024).decode()
                    print("Response\n")
                    print(response)
                    print("\n\n")

                    
            else:
                print("Authentication failed")

        except Exception as e:
            print(f"Error: {e}")
            break

        finally:
            pass

