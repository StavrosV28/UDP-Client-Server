# Stavros Varvatsoulis
# CSCI 348: Data Communications
# FALL 2024 Semester
# Project 1: A Chat Application over UDP

from socket import *
import threading

clients = {}  # Dictionary to maintain online clients: {username: (address)}

# Handles the commands like join, leave, users, and to
def handle_client_message(data, address, sock):
    global clients
    # We decode the messages coming from client here
    try:
        message = data.decode().strip()
        parts = message.split(":", 1)
        command = parts[0].lower() # Extract the command whether it is join, leave etc.

        # Add user to chat
        if command == "join":
            username = parts[1]
            clients[username] = address # Store user address in clients
            print(f"{username} joined the chat.")
            # Notify user they are in the chat now
            sock.sendto("You are now in the chat.".encode(), address)
        
        # Removes user from the server/chat...
        elif command == "leave":
            username = parts[1]
            if username in clients:
                del clients[username] # Take user out of dict
                print(f"{username} left the chat.")
                sock.sendto("Bye.".encode(), address)

        # Check all connected users
        elif command == "users":
            user_list = ", ".join(clients.keys())
            sock.sendto(f"Users connected:{user_list}".encode(), address)

        # Sends a message to specific user or more than one user
        elif command.startswith("to"):
            recipients_and_msg = parts[1].split(" msg ", 1)
            recipients = recipients_and_msg[0].split()  # Split recipients here
            msg = recipients_and_msg[1]
            # We find the username of the sender based on their address here
            sender = next((user for user, addr in clients.items() if addr == address), None)

            # Send a message to every user connected to server
            if "all" in recipients:
                for recipient, addr in clients.items():
                    if recipient != sender: # Will not send to sender
                        sock.sendto(f"{sender} says: <{msg}>".encode(), addr)
            # In case we are sending to specific users (i.e. "to joe jill msg Hi.")
            else:
                for recipient in recipients:
                    if recipient == sender:
                        continue  # Skip sending to the sender
                    if recipient in clients:
                        sock.sendto(f"{sender} says: <{msg}>".encode(), clients[recipient])
                    else:
                        # Sender is notified that the user is not online
                        sock.sendto(f"Error:<{recipient} is not online!!>".encode(), address)
    except Exception as e:
        print(f"Error handling message: {e}")  # Log error but we want server to keep running

# This will start the UDP server for clients to join to
def udp_server():
    sock = socket(AF_INET, SOCK_DGRAM)
    server_address = ('', 20000)
    sock.bind(server_address)
    print('Chat server is up and listening on port 20000')

    while True:
        try:
            data, address = sock.recvfrom(65507)
            # This will make a new thread to handle the clients message
            # This helps keep up with simultaneous requests without blocking the server
            threading.Thread(target=handle_client_message, args=(data, address, sock)).start()
        except ConnectionResetError:
            # Suppress the ConnectionResetError to avoid displaying the irrelevant error
            pass
        except Exception as e:
            pass


if __name__ == "__main__":
    udp_server()
