"""
The protocol:
    Server:
        - After receiving registering information from the client, server send the unit id of client, the tcp port and the interval to the client.
        - Server can send message to the client through the udp port client sent.
    Reply to registering packets:
        "!SUCCEEDED + info"
        or "!FAILED + error"


On connection:
    Client:
        First send a TCP packet to request the connection
        Then send the
    Server:
        After recieving the 

Clean disconnection:
    Sent the message "!DISCONNECT" to confirm clients' disconnection.

The first message send to the server must be in length of 64 bytes, indicating the length of the messages.
"""

import socket
import threading
from requests import get

HEADER = 16
PORT = 34567

SERVER = "192.168.0.101"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

# family: internet. sending data with tcp protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding server to the address
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while (connected):
        raw_msg = conn.recv(256)
        msg_length = raw_msg[0:HEADER].decode(FORMAT) # first 16 bytes
        if msg_length:
            msg_length = int(msg_length)
            print(f"The length of the msg: {msg_length}")
            msg = raw_msg[HEADER:].decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            
            print(f"[{addr}] {msg}")
            conn.send("Msg received!".encode(FORMAT))
        
    conn.close()

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")

#     connected = True
#     while (connected):
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)
#             if msg == DISCONNECT_MSG:
#                 connected = False

#             print(f"[{addr}] {msg}")
#             conn.send("Msg received".encode(FORMAT))

#     conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 2}")

def inputCommand():
    while True:
        command = input()
        if (command == "TRUE"):
            print("Command received, this is TRUE")
        if (command == "FALSE"):
            break;
        

print("[STARTING] Server is starting...")
thread_listening = threading.Thread(target=start)
thread_input = threading.Thread(target=inputCommand)
thread_listening.start()
thread_input.start()