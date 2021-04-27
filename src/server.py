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

# Dependencies
import socket
import threading
import json
import netifaces
from requests import get
from datetime import datetime



# Length of the field in the message
HEADER = 16
CMD = 5

# Port number
TCP_PORT = 34567
UDP_PORT = 45678


# Getting the server's IP address dynamically
# iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
# SERVER = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
SERVER = ""
def findIP():
    global SERVER
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    SERVER = s.getsockname()[0]
    s.close()

findIP()
TCP_ADDR = (SERVER, TCP_PORT)
# UDP_ADDR = (SERVER, UDP_PORT)
FORMAT = 'utf-8'

REGISTER_MSG = "!RGTR"
DISCONNECT_MSG = "!DISC"
SUCCEEDED_MSG = "!SUCC"
FAILED_MSG = "!FAIL"
INFO_MSG = "!INFO"
UPDATE_MSG = "!UPDT"

packet_length = 1024
no_of_connection = 0

client_info = {}
client_id = 0
default_interval = 10
# family: internet. sending data with tcp protocol
server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sending updates by udp ports
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# binding server to the address
server_tcp.bind(TCP_ADDR)
# server_udp.bind(UDP_ADDR)

def handle_client(conn, addr):
    global no_of_connection
    global packet_length
    global client_info
    global default_interval
    global client_id

    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while (connected):
        raw_msg = conn.recv(packet_length)
        msg_length = raw_msg[0:HEADER].decode(FORMAT) # first 16 bytes
        if msg_length:
            msg_length = int(msg_length)
            print(f"The length of the msg: {msg_length}")
            cmd = raw_msg[HEADER:HEADER+CMD].decode(FORMAT)
            print(f"The type of the msg: {cmd}")
            if cmd == DISCONNECT_MSG:
                conn.send("!DISC: RECEIVED".encode(FORMAT))
                connected = False
                no_of_connection -= 1

            msg = raw_msg[HEADER+CMD:].decode(FORMAT)
            if cmd == REGISTER_MSG:
                print(f"Message: {msg}")
                info = json.loads(msg)

                # can remove this later
                print(type(info))

                # Adding new client info
                key = str(client_id)
                client_info[key] = info
                print(client_info[key]["name"])
                print(client_info[key]["ip"])
                print(client_info[key]["UDP_port"])
                print(client_info[key]["time"])
                client_info[key]["interval"] = default_interval

                server_info = {
                    "client_id" : client_id,
                    "port" : TCP_PORT,
                    "interval" : default_interval
                }

                msg = json.dumps(server_info)

                message = (SUCCEEDED_MSG + msg).encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                conn.send(send_length + message)
                
                # increase the client id
                client_id += 1

            if cmd == INFO_MSG:
                print(f"[{addr}] {msg}")
                conn.send("!INFO: RECEIVED".encode(FORMAT))
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)
        
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

def tcp_start():
    global no_of_connection
    server_tcp.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server_tcp.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        no_of_connection += 1
        thread.start()
        print(f"[ACTIVE CONNECTION] {no_of_connection}")

def input_command():
    global client_info
    
    info = {}
    client_id = ""
    while True:
        command = input()
        if (command == "UPDATE"):
            # Currently testing for single client
            number_of_client = len(client_info)        
            # find client id 
            while True:
                client_id = input("Enter the client id: ")
                # gotta handle the int key checker too
                if (client_id in client_info):
                    info = client_info[client_id]
                    print(info)
                    break
                else:
                    print("Client id not found, please try again!")

            interval = 0
            # get the desire interval
            while True:
                try:
                    # Convert it into integer
                    value = input("Enter the interval: ") 
                    interval = int(value)
                    break
                except ValueError:
                    print("Please enter an integer.")
            # send the interval to the client
            msg = (UPDATE_MSG + str(interval)).encode(FORMAT)
            msg_length = len(msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            server_udp.sendto(send_length + msg, (info["ip"], info["UDP_port"]))
            client_info[client_id]["interval"] = interval
            
        if (command == "FALSE"):
            break;

        

print("[STARTING] Server is starting...")
thread_listening = threading.Thread(target=tcp_start)
thread_input = threading.Thread(target=input_command)
thread_listening.start()
thread_input.start()