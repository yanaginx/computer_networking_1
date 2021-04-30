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
# import netifaces
import shortuuid
import os
import psutil
import time
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

TCP_ADDR = (SERVER, TCP_PORT)
UDP_ADDR = (SERVER, UDP_PORT)
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
current_system_pid = os.getpid()

slot = ["","","",""]
active_slot = [0,0,0,0]
screen = ""
screen_header = ""

command =""
command_signal = 0

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
    global screen_header
    global slot
    global active_slot

    slot_id = 0
    connected = True
    current_id = shortuuid.uuid()

    header = f"[NEW CONNECTION] {addr} connected.\n"
    timestart = time.time()
    for i in range(len(active_slot)):
        if not active_slot[i]:
            active_slot[i] = 1
            slot_id=i
            break
    slot[slot_id] = header
    while (connected):
        raw_msg = ""
        try: 
            raw_msg = conn.recv(packet_length)
        except:
            slot[slot_id]="Client is not listenable. Closing the connection..."
            connected = False
            active_slot[slot_id] = 0
            no_of_connection -= 1
            break

        msg_length = raw_msg[0:HEADER].decode(FORMAT) # first 16 bytes
        if msg_length:
            slot[slot_id] = header
            try:
                msg_length = int(msg_length)
                slot[slot_id]+=f"The length of the msg: {msg_length}\n"
                cmd = raw_msg[HEADER:HEADER+CMD].decode(FORMAT)
                slot[slot_id]+=f"The type of the msg: {cmd}\n"
                if cmd == DISCONNECT_MSG:
                    conn.send("!DISC: RECEIVED".encode(FORMAT))
                    connected = False
                    active_slot[slot_id] = 0
                    no_of_connection -= 1

                msg = raw_msg[HEADER+CMD:].decode(FORMAT)
                if cmd == REGISTER_MSG:
                    slot[slot_id]+=f"Message: {msg}\n"
                    try:
                        info = json.loads(msg)
                        # can remove this later
                        slot[slot_id]+=str(type(info))+"\n"
                        # Adding new client info
                        client_info[current_id] = info
                        slot[slot_id]+=client_info[current_id]["name"]+"\n"
                        slot[slot_id]+=client_info[current_id]["ip"]+"\n"
                        slot[slot_id]+=str(client_info[current_id]["UDP_port"])+"\n"
                        slot[slot_id]+=client_info[current_id]["time"]+"\n"
                        client_info[current_id]["interval"] = default_interval

                        server_info = {
                            "client_id" : current_id,
                            "tcp_port" : TCP_PORT,
                            "interval" : default_interval
                        }

                        msg = json.dumps(server_info)

                        message = (SUCCEEDED_MSG + msg).encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        try:
                            conn.send(send_length + message)
                        except Exception as e:
                            slot[slot_id]+=f"Exception when sending confirmation: {e}\n"
                            break

                    except ValueError:
                        slot[slot_id]+=f"Decoding JSON has failed. Prompting client the error\n"
                        msg = "Wrong format"
                        message = (FAILED_MSG + msg).encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        try:
                            conn.send(send_length + message)
                        except Exception as e:
                            slot[slot_id]+=f"Exception when sending confirmation: {e}\n"
                            break                   

                if cmd == INFO_MSG:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    slot[slot_id]+=f"ID: {current_id}\n"
                    slot[slot_id]+=f"Current Time = {current_time}\n"
                    slot[slot_id]+=f"{msg}"
                    try: 
                        conn.send("!INFO: RECEIVED".encode(FORMAT))
                    except Exception as e:
                        slot[slot_id]+=f"Exception when sending confirmation: {e}\n"
                        break

            except ValueError:
                slot[slot_id]+=f"The message length is not recognizable! Abort the message\n"     
            slot[slot_id]+=f"Time elapsed: {time.time()-timestart}\n"
    conn.close()
    client_info.pop(current_id, None)
    active_slot[slot_id] = 0
    # print current client_info
    # slot[slot_id]=str(client_info)+"\n"
    slot[slot_id]+="Connection closed\n"

    screen_header=f"[LISTENING] Server is listening on {SERVER}\n" + f"[ACTIVE CONNECTION] {no_of_connection}\n"


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
    global screen_header
    global screen
    server_tcp.listen()
    screen_header=f"[LISTENING] Server is listening on {SERVER}\n" + f"[ACTIVE CONNECTION] {no_of_connection}\n"
    while True:
        screen_header=f"[LISTENING] Server is listening on {SERVER}\n" + f"[ACTIVE CONNECTION] {no_of_connection}\n"
        conn, addr = server_tcp.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        no_of_connection += 1
        thread.start()

def input_command():
    global client_info
    global command_signal
    global command
    global screen
    global screen_header
    while True:
        info = None
        client_id = ""
        screen = screen_header
        if command_signal:
            command_signal = 0
            if (command == "UPDATE"):
                # Currently testing for single client
                number_of_client = len(client_info)        
                # find client id s
                while True:
                    screen = screen_header + "Enter the client id: "
                    if command_signal:
                        command_signal = 0
                        if (command == 'cancel'):
                            break
                        # gotta handle the int key checker too
                        if (command in client_info):
                            info = client_info[command]
                            screen += str(info)
                            break
                        else:
                            screen += "Client id not found, please try again: "
                if (info):
                    interval = 0
                    # get the desire interval
                    while True:
                        screen = screen_header + "Enter the interval: \n"
                        if command_signal:
                            command_signal = 0
                            if (command == 'cancel'):
                                break
                            try:
                                interval = int(command)
                                print(interval)
                                break
                            except ValueError:
                                screen = screen_header + "Please enter an integer. \n"
                    # send the interval to the client
                    if not command == 'cancel':
                        msg = (UPDATE_MSG + str(interval)).encode(FORMAT)
                        msg_length = len(msg)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        t_end = time.time() + 10
                        # while time.time() < t_end:
                        server_udp.sendto(send_length + msg, (info["ip"], info["UDP_port"]))
                            # if receive the message then break
                        # client_info[client_id]["interval"] = interval
                
            if (command == "CLOSE"):
                screen += screen_header + "Closing the server...\n"
                ThisSystem = psutil.Process(current_system_pid)
                ThisSystem.terminate()
                break;

def server_start():  
    global screen_header   
    findIP()
    screen_header = "[STARTING] Server is starting...\n"
    thread_listening = threading.Thread(target=tcp_start,daemon=True)
    thread_input = threading.Thread(target=input_command,daemon=True)
    thread_listening.start()
    thread_input.start()

