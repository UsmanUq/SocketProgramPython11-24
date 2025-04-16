# SocketProgramPython11-24

# 💬 Python Socket-Based Chat Application

A real-time, multi-client chat application built in Python using sockets and threading, with a `tkinter` GUI for the client and advanced features like private messaging, chat history logging, and reconnection support.

---

## 📌 Features

- ✅ Multi-client support using threading
- ✅ Real-time message broadcasting
- ✅ Private messaging (`/msg <nickname> <message>`)
- ✅ GUI chat interface using `tkinter`
- ✅ Message tagging with color codes (public, private, system)
- ✅ Client reconnect feature (`/rejoin`)
- ✅ Graceful exit (`/exit`)
- ✅ Chat history saved on the server

---

## 🧠 Technologies Used

| Technology | Purpose                     |
|------------|-----------------------------|
| Python     | Core language               |
| `socket`   | Network communication       |
| `threading`| Concurrent client handling  |
| `tkinter`  | GUI for the client          |
| `datetime` | Timestamps for messages     |

---

## 🖥️ Architecture

```
+-------------+       +-------------+
|  Client 1   |<----->|             |
+-------------+       |             |
                      |             |
+-------------+       |   Server    |-----> Chat History File
|  Client 2   |<----->|             |
+-------------+       |             |
                      |             |
+-------------+       +-------------+
|  Client 3   |<----->  Handles:
+-------------+           • Broadcasting
                         • Private Messaging
                         • Logging History
```

---

## 📷 GUI Preview

- **Color-coded messages:**
  - 💬 **Public (blue)**: from other users
  - 🔐 **Private (purple)**: direct messages
  - ⚙️ **System (green)**: join/leave notices

- **Components:**
  - Chat window with scroll
  - Text input field
  - Send button
  - Enter-key binding

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.7+
- OS: Windows/Linux/macOS

### 📁 Clone the repository

```bash
git clone https://github.com/your-username/python-socket-chat-app.git
cd python-socket-chat-app
```

---

## 🛠️ How to Run

### 🖥️ Start the Server

```bash
python server.py
```

You should see:
```bash
Server started and listening on 127.0.0.1:5555
```

### 💬 Run the Client (in a new terminal)

```bash
python client.py
```

Enter your **nickname** when prompted and enjoy chatting!

You can open multiple terminals to simulate multiple users.

---

## 💡 Commands

| Command             | Description                          |
|---------------------|--------------------------------------|
| `/msg <name> <msg>` | Send a private message               |
| `/exit`             | Leave the chatroom                   |
| `/rejoin`           | Reconnect to the chat after leaving  |

---

## 📂 File Structure

```
├── client.py            # Client-side application (GUI)
├── server.py            # Server-side application
├── chat_history.txt     # Chat log (auto-created by server)
└── README.md            # Project documentation
```

---

## 🧪 Testing

- ✅ Verified with up to 20 concurrent clients
- ✅ Message delivery (public & private)
- ✅ Chat log correctness
- ✅ GUI responsiveness under load
- ✅ Reconnect behavior after `/exit`

---

## 🔒 Future Improvements

- User authentication/login system
- End-to-end encryption for messages
- Online user list display in GUI
- Chat history retrieval in the client

---

## 📃 License

This project is open source under the [MIT License](LICENSE).

---

## 👨‍💻 Author

built for CN in 5th semester 32868
Feel free to fork, contribute, or report bugs!



---
