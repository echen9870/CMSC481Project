import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Client {
    private static final String SERVER_ADDRESS = "172.21.2.5";
    private static final int SERVER_PORT = 12345;

    public static void main(String[] args) {
        Socket socket;
        PrintWriter out;
        BufferedReader in;
        BufferedReader stdIn;
        try {
            socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            stdIn = new BufferedReader(new InputStreamReader(System.in));
            try {
                // Send the username to identify the client
                System.out.print("Enter username: ");
                String username = stdIn.readLine();
                out.println(username);

                // Receive the challenge token from the server
                String challengeToken = in.readLine().trim();

                // Generate the response by appending the password to the challenge token and
                // calculating the MD5 hash
                System.out.print("Enter password: ");
                String password = stdIn.readLine();
                String hashMessage = challengeToken + password;
                String responseHash = getMD5Hash(hashMessage);
                
                System.out.println(responseHash);
                // Send the response to the server
                out.println(responseHash);

                // Receive the authentication result from the server
                String authResult = in.readLine().trim();

                // Display the authentication result
                if ("200 SUCCESS".equals(authResult)) {
                    System.out.println("Authentication successful");

                    // Loop for sending commands to the server
                    while (true) {
                        String message = getUserInput(username, stdIn);
                        out.println(message);

                        String response = in.readLine();
                        System.out.println("Response:");
                        System.out.println(response);

                        if (message.contains("Exit")) {
                            socket.close();
                            break;
                        }
                    }
                } else {
                    System.out.println(authResult);
                }
            } catch (IOException e) {
                System.err.println("Error: " + e.getMessage());
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String getUserInput(String username, BufferedReader stdIn) throws IOException {
        System.out.print(
                "Enter the type of command you would like to execute (Create, Read, Delete, Update) or type Exit to exit:");
        String command = stdIn.readLine();

        while (true) {
            // Create Command
            if ("Exit".equals(command)) {
                return username + ";Exit;Exit";
            } else if ("Create".equals(command)) {
                System.out.print("What is the name of the task:");
                String taskName = stdIn.readLine();
                return username + ";Create;" + taskName;
            } else if ("Read".equals(command)) {
                System.out.print("What is the task you want to read (Leave -1 to read all tasks):");
                String taskID = stdIn.readLine();
                return username + ";Read " + taskID + ";";
            } else if ("Delete".equals(command)) {
                System.out.print("What is the id of the task to delete (Leave -1 to delete all tasks):");
                String taskID = stdIn.readLine();
                return username + ";Delete " + taskID + ";";
            } else if ("Update".equals(command)) {
                System.out.print("What is the id of the task to update:");
                String taskID = stdIn.readLine();
                System.out.print("What is the new name of the task:");
                String taskName = stdIn.readLine();
                return username + ";Update " + taskID + ";" + taskName;
            } else {
                System.out.println("Command is not valid, try again.");
                System.out.print(
                        "Enter the type of command you would like to execute (Create, Read, Delete, Update) or type Exit to exit:");
                command = stdIn.readLine();
            }
        }
    }

    private static String getMD5Hash(String message) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] bytes = md.digest(message.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : bytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }
}
