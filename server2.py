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

# Function to handle clients
def handle_client(client_socket):
    try:
        # First, receive and set the nickname
        nickname = client_socket.recv(1024).decode('utf-8')
        with lock:
            clients[client_socket] = nickname
        print(f"{nickname} has joined the chat!")
        broadcast(f"[System] {nickname} has joined the chat!".encode('utf-8'), client_socket)

        while True:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message == "/exit":  # Check for exit command
                print(f"{nickname} has left the chat.")
                break

            if message.startswith("/msg"):
                # Handle private messaging
                try:
                    _, recipient, private_message = message.split(" ", 2)
                    send_private_message(client_socket, recipient, private_message)
                except ValueError:
                    client_socket.send("Invalid private message format. Use /msg <nickname> <message>".encode('utf-8'))
            else:
                # Handle public broadcasting
                formatted_message = f"[{datetime.now().strftime('%H:%M:%S')}] {clients[client_socket]}: {message}"
                print(formatted_message)  # Print to server console
                broadcast(formatted_message.encode('utf-8'), client_socket)
                save_chat_history(formatted_message)
    except (ConnectionResetError, BrokenPipeError):
        print(f"{nickname} was disconnected unexpectedly.")
    finally:
        # Remove the client from the list and notify others
        with lock:
            nickname = clients.pop(client_socket, "A user")
        broadcast(f"[System] {nickname} has left the chat.".encode('utf-8'))
        client_socket.close()

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