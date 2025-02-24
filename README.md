Here is a **README** description for your **UDPClient/Server Chat Application** that you can use for your GitHub repository:

---

# UDP Chat Application

This project is a **simple chat application** implemented over **UDP (User Datagram Protocol)**. The application consists of a **UDP server** that manages chat participants and a **UDP client** that allows users to join the chat, check online users, and send direct or group messages.

## Features

- **User Registration**: Clients can join the chat by specifying a username.
- **Private Messaging**: Users can send direct messages to specific participants.
- **Group Messaging**: Messages can be broadcasted to all users in the chat.
- **User List**: Clients can request a list of currently connected users.
- **Graceful Exit**: Users can leave the chat, and the server updates the list of active participants.

## How It Works

### Server (`UDPServer.py`)

- Listens on port **20000** for incoming messages from clients.
- Handles client commands such as:
  - `JOIN:<username>` → Adds a user to the chat.
  - `LEAVE:<username>` → Removes a user from the chat.
  - `USERS:` → Responds with a list of currently connected users.
  - `TO <usernames> MSG <message>` → Sends a message to specific users or to all users if "all" is included.

### Client (`UDPClient.py`)

- Connects to the server and allows users to:
  - **Join the chat** by entering a username.
  - **Send messages** using the `to <usernames> msg <message>` format.
  - **Check online users** by typing `users`.
  - **Leave the chat** by typing `leave`.

## Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/udp-chat-app.git
   cd udp-chat-app
   ```

2. **Run the Server**:
   ```bash
   python UDPServer.py
   ```
   The server will start listening on **port 20000**.


3. **Run a Client**:
   ```bash
   python UDPClient.py
   ```
   - Enter a username to join the chat.
   - Use commands like `users`, `leave`, or `to <username> msg <message>` to interact.

4. **Run Multiple Clients**:
   - Open multiple terminal windows and start multiple clients to simulate a multi-user chat.


## Notes

- The client uses `select` for non-blocking input handling.
- The server uses threading to handle multiple clients simultaneously.
- Messages are **not encrypted**, making this project a basic demonstration of UDP-based communication.

---
