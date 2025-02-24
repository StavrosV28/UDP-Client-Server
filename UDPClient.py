# Stavros Varvatsoulis
# CSCI 348: Data Communications
# FALL 2024 Semester
# Project 1: A Chat Application over UDP

from socket import *
import os
import select

BUFFER_SIZE = 65507
buffer = []

def checkKeyboardInput():
    if os.name == 'nt':  # Windows
        import msvcrt
        if msvcrt.kbhit():  # Check if a key has been pressed
            ch = msvcrt.getwch()  # Get a single character from input
            print(ch, end='', flush=True)
            if ch == '\r':  # Enter key
                print(flush=True)
                line = "".join(buffer)
                buffer.clear()
                return line
            elif ch == '\b':  # Backspace
                if len(buffer) > 0:
                    buffer.pop()
                    line = "".join(buffer)
                    print(f"\b \b", end='', flush=True)
                    print(f"\r{line}", end='', flush=True)
            else:
                buffer.append(ch)
    return None

# Client-server
def main():
    client_sock = socket(AF_INET, SOCK_DGRAM)
    server_address = ('127.0.0.1', 20000)

    # User enters their username
    username = input("Enter your username: ").strip()
    # Sends to server that said user joined
    client_sock.sendto(f"JOIN:{username}".encode(), server_address)

    while True:
        try:
            # Check for incoming messages from the server
            read_sockets, _, _ = select.select([client_sock], [], [], 0.05)
            
            # Process messages from the server
            for sock in read_sockets:
                if sock == client_sock:
                    data, _ = client_sock.recvfrom(BUFFER_SIZE)
                    print(data.decode())

            # Check for user input using func provided "checkKeyboardInput"
            command = checkKeyboardInput()
            if command:
                command = command.strip()
                if command.lower() == "leave":
                    # Notifies server that a user has left
                    client_sock.sendto(f"LEAVE:{username}".encode(), server_address)
                    print("You have left the chat.")
                    client_sock.close() # That client exits...from program
                    return
                elif command.lower() == "users":
                    # Sends to server in response to the command
                    client_sock.sendto("USERS:".encode(), server_address)
                elif command.lower().startswith("to"):
                    client_sock.sendto(f"TO:{command[3:]}".encode(), server_address)
        except ConnectionResetError:
            print("Connection closed by the server.")
            client_sock.close()
            return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
