Members:
Eric Chen, CS24819
Peter Jacquet, ZL30817

Time to Complete: 4 - 5 Weeks

Summary Of Learning:
 - Learned how to authenticate with hashes
 - Learned how to manage multiple clients on a single thread with the use of epoll
 - Setting up and running docker containers that simulated a network

Learning Challenges:
 - Learning how to debug network failures, we had to use a lot of try catch blocks
 - Epolling was really tricky to learn, had to watch many videos and tutorials


How to Setup 
1. Run the network.yml file to setup the network
2. Make sure the hA container is able to compile and run Java files if using the client.java file
3. Copy the client file (client.py or client.java) to the hA container and copy the server file to the hB container
4. Run the server file before running the client file

Network
- The network.yml that is included in the repository/submission was the one used to setup the network and docker containers
Enviroment
- The client program is hardcoded with IP Address and the server is hardcoded with ports

Application
- The application is a simple task list program. A user is able to login, and each user has their respective task list
- A task list is capable of CRUD tasks
- Only a unique usernames are allowed to be logged in at a single time. This prevents multiple users with the same username to be logged in at the same time
- Concurrency is handled through e-polling

Message Formats
- Client Side Messages are of format username;command;text
- Usernames are used in order to identify which task list has to be modified
- Command is used to identify the type of instruction to perform
- The text is only used when creating or updating commands
- Inputs parsing are handled on the client side, so the server can expect the commands sent by the client to be good
- There is no TCP streaming capabilities
- Server Side Responses are just basic String Messages




