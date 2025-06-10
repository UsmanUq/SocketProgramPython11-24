import socket
import threading
from datetime import datetime

# Dictionary to store clients and their nicknames
clients = {}
lock = threading.Lock()

# Save chat history in separate text file
def save_chat_history(message):
    with open("chat_history.txt", "a") as file:
        file.write(message + "\n")

# Function to broadcast messages to all clients
def broadcast(message, sender_socket=None):
    with lock:
        for client_socket in list(clients.keys()):
            if client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except:
                    print(f"Error sending message to {clients.get(client_socket, 'Unknown')} — Removing from clients.")
                    client_socket.close()
                    clients.pop(client_socket, None)

# Send private messages to recipients
def send_private_message(sender_socket, recipient_nickname, message):
    with lock:
        for client_socket, nickname in clients.items():
            if nickname == recipient_nickname:
                try:
                     client_socket.send(f"[Private] {clients[sender_socket]}: {message}".encode('utf-8'))
                    #client_socket.send(f"[{datetime.now().strftime('%H:%M:%S')}] [Private] {clients[sender_socket]}: {message}".encode('utf-8'))
                except:
                    client_socket.close()
                    clients.pop(client_socket, None)
                return  
    sender_socket.send(f"User '{recipient_nickname}' not found.".encode('utf-8'))
    print(f"Sending private message: [Private] {clients[sender_socket]}: {message}")
    

def handle_client(client_socket):
    global master_socket  # Keep track of the master
    try:
        # First, receive and set the nickname
        nickname = client_socket.recv(1024).decode('utf-8')
        with lock:
            clients[client_socket] = nickname
            if not 'master_socket' in globals():
                master_socket = client_socket
                print(f"'{nickname}' is now the master.")
                client_socket.send("[System] You are the master and can kick users with /kick <nickname>.".encode('utf-8'))

        print(f"{nickname} has joined the chat!")
        broadcast(f"[System] {nickname} has joined the chat!".encode('utf-8'), client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')

            if message == "/exit":
                print(f"{nickname} has left the chat.")
                break

            # Check if it's a kick command
            if message.startswith("/kick"):
                if client_socket == master_socket:
                    try:
                        _, target_nickname = message.split(" ", 1)
                        kick_user(target_nickname, client_socket)
                    except ValueError:
                        client_socket.send("Invalid kick command format. Use /kick <nickname>".encode('utf-8'))
                else:
                    client_socket.send("You are not the master. Only the master can kick users.".encode('utf-8'))
                continue

            # Check if it's a private message
            if message.startswith("/msg"):
                try:
                    _, recipient, private_message = message.split(" ", 2)
                    send_private_message(client_socket, recipient, private_message)
                except ValueError:
                    client_socket.send("Invalid private message format. Use /msg <nickname> <message>".encode('utf-8'))
                continue

            # Broadcast normal message
            formatted_message = f"[{datetime.now().strftime('%H:%M:%S')}] {nickname}: {message}"
            print(formatted_message)
            broadcast(formatted_message.encode('utf-8'), client_socket)
            save_chat_history(formatted_message)

    except (ConnectionResetError, BrokenPipeError):
        print(f"{nickname} was disconnected unexpectedly.")
    finally:
        # Remove client and notify others
        with lock:
            nickname = clients.pop(client_socket, "A user")
        broadcast(f"[System] {nickname} has left the chat.".encode('utf-8'))
        client_socket.close()

# Kick function
def kick_user(nickname, master_socket):
    with lock:
        for client_socket, client_nickname in list(clients.items()):
            if client_nickname == nickname:
                client_socket.send("[System] You have been kicked from the chat.".encode('utf-8'))
                client_socket.close()
                clients.pop(client_socket, None)
                broadcast(f"[System] {nickname} has been kicked by the master.".encode('utf-8'))
                print(f"{nickname} has been kicked by the master.")
                return
        master_socket.send(f"User '{nickname}' not found.".encode('utf-8'))





# Start the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 5555))
server_socket.listen(5)
print("Server started and listening on 127.0.0.1:5555")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")

    # Start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
#strat the server
start_server()