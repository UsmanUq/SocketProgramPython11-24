import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


def receive_messages():
    global connected
    while connected:
        try:
            # Receive message from server
            message = client_socket.recv(1024).decode('utf-8')
            
            # Display the message in the chat window
                        # Detect the type of message and apply the appropriate tag
            if message.startswith("[Private]"):
                tag = "private"
            elif message.startswith("[System]"):
                tag = "system"
            else:
                tag = "user"

            # Display the message with the tag
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, message + "\n", tag)
            chat_window.config(state=tk.DISABLED)
            chat_window.yview(tk.END)  # Scroll to the latest message

        except:
            if connected:  # Avoid redundant messages
                chat_window.config(state=tk.NORMAL)
                chat_window.insert(tk.END, "Disconnected from server.\n")
                chat_window.config(state=tk.DISABLED)
            break


def send_messages(event=None):
    global connected, client_socket
    message = input_box.get()
    input_box.delete(0, tk.END)  # Clear the input box after sending

    if message.strip() == "/exit":
        connected = False
        client_socket.send(message.encode('utf-8'))
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You have left the chatroom. Type '/rejoin' to reconnect.\n")
        chat_window.config(state=tk.DISABLED)
        client_socket.close()
    elif message.strip() == "/rejoin":
        if not connected:
            try:
                # Reconnect logic
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(("127.0.0.1", 5555))
                client_socket.send(nickname.encode('utf-8'))
                connected = True

                # Restart receiving messages
                receive_thread = threading.Thread(target=receive_messages)
                receive_thread.daemon = True
                receive_thread.start()

                chat_window.config(state=tk.NORMAL)
                chat_window.insert(tk.END, "Reconnected to the chatroom.\n")
                chat_window.config(state=tk.DISABLED)
            except Exception as e:
                chat_window.config(state=tk.NORMAL)
                chat_window.insert(tk.END, f"Failed to reconnect: {e}\n")
                chat_window.config(state=tk.DISABLED)
    else:
        if connected:
            client_socket.send(message.encode('utf-8'))



def connect_to_server():
    global client_socket, connected, nickname, input_box, chat_window

    # Connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))
    connected = True

    # Get nickname
    nickname = input("Enter your nickname: ")
    client_socket.send(nickname.encode('utf-8'))

    # Create GUI
    root = tk.Tk()
    root.title(nickname)

    # Chat window
    chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    chat_window.config(state=tk.DISABLED)
    chat_window.pack(padx=10, pady=10)

    # Add tag configurations here
    chat_window.tag_config("user", foreground="blue")
    chat_window.tag_config("private", foreground="purple")
    chat_window.tag_config("system", foreground="green")

    # Input box
    input_box = tk.Entry(root, width=40)
    input_box.pack(padx=10, pady=10, side=tk.LEFT)

    # Bind Enter key to send messages
    input_box.bind("<Return>", send_messages)

    # Send button (optional)
    send_button = tk.Button(root, text="Send", command=send_messages)
    send_button.pack(padx=10, pady=10, side=tk.RIGHT)

    # Start thread for receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    # Run the GUI event loop
    root.mainloop()

# Start the client
connect_to_server()