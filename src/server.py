"""
The protocol:
    Server:
        - After receiving registering information from the client, server send the unit id of client, the tcp port and the interval to the client.
        - Server can send message to the client through the udp port client sent.
    Reply to registering packets:
        "!SUCC + [info]"
        or "!FAIL + [error]"

Clean disconnection:
    Sent the message "!DISC" to confirm clients' disconnection.

The first message send to the server must be in length of 64 bytes, indicating the length of the messages.
Consider adding semaphore or mutex for the common database (storing senders' informations).
"""

import socket
import threading
import json
from requests import get

HEADER = 16
CMD = 5
PORT = 34567

SERVER = "192.168.0.101" # Change the address whenever you want to test on your machine
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
REGISTER_MSG = "!RGTR"
DISCONNECT_MSG = "!DISC"
SUCCEEDED_MSG = "!SUCC"
FAILED_MSG = "!FAIL"
INFO_MSG = "!INFO"
packet_length = 256
no_of_connection = 0

# family: internet. sending data with tcp protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sending updates by udp ports

# binding server to the address
server.bind(ADDR)

def handle_client(conn, addr):
    global no_of_connection
    global packet_length
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    no_of_connection += 1

    while (connected):
        raw_msg = conn.recv(packet_length)
        msg_length = raw_msg[0:HEADER].decode(FORMAT) # first 16 bytes
        if msg_length:
            msg_length = int(msg_length)
            print(f"The length of the msg: {msg_length}")
            cmd = raw_msg[HEADER:HEADER+CMD].decode(FORMAT)
            print(f"The type of the msg: {cmd}")
            if cmd == DISCONNECT_MSG:
                connected = False
                no_of_connection -= 1

            msg = raw_msg[HEADER+CMD:].decode(FORMAT)
            if cmd == REGISTER_MSG:
                print(f"Message: {msg}")
                info = json.loads(msg)
                print(info["name"])
                print(info["ip"])
                print(info["UDP_port"])
                print(info["time"])
                conn.send(SUCCEEDED_MSG.encode(FORMAT))

            if cmd == INFO_MSG:
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