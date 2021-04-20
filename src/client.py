# -*- coding: future_fstrings -*-
import socket
import ntplib
import time
import psutil
import pickle
import json
from datetime import datetime


"""
Client's dependencies (linux distros ver):
    ntplib
    psutil

Install these using pip
"""

"""
The protocol:
Client: 
    Send its registering information through TCP, including its Name, IP addr, UDP port (to recieve server's info), current date/time 
        
Registering packet: "!RGTR + info"
Disconnecting packet: "!DISC"

// Considering using pickle on packing the data (using json now)

Client's sending data:
	CPU temp, Disk drive's usage, RAM's usage
        CPU temp: using psutil 
        Disk drive's usage: using psutil
        RAM's usage: 
    Header (indicating the length of the data is 16 bytes)
    Command abbriviate: 5 bytes 
    Length of the sending data is no longer than 240 bytes
    
Msg format: 
    [msg's length] + [5 bytes command abbriviation] + [data]
"""


# VARIABLE DEFINITION
HEADER = 16
SERVER = "192.168.0.101" # change the address whenever you want to test on your machine
PORT = 34567 # to send the register info
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
SEND_PORT = 0
DISCONNECT_MSG = "!DISC"
REGISTER_MSG = "!RGTR"
INFO_MSG = "!INFO"
SUCCEEDED_MSG = "!SUCC"
FAILED_MSG = "!FAIL"
reg_succeeded = False


# METHOD IMPLEMENTATION

# this is hardcoded (no good), will find ways to code it better afterward
def get_CPU_temp():
    return f"CPU temperature: {psutil.sensors_temperatures()['coretemp'][0].current}\n"

def get_disk_usage():
    return f"disk % used: {psutil.disk_usage('/')[3]}\n"

def get_RAM_usage():
    return f"memory % used: {psutil.virtual_memory()[2]}\n"

def send(cmd, msg):
    global reg_succeeded
    message = (cmd + msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_send.send(send_length + message)
    if cmd == REGISTER_MSG:
        response = client_send.recv(256).decode(FORMAT)
        if response == "!SUCC":
            reg_succeeded = True

    if cmd == INFO_MSG and reg_succeeded:
        print(client_send.recv(256).decode(FORMAT))
        

#=====================================================

# Sending 
client_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_send.connect(ADDR)

# Receiving
client_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_name = socket.gethostname()
ip_addr = socket.gethostbyname(client_name)
client_recv.bind((ip_addr, 0))
udp_port = client_recv.getsockname()[1]

info = {
    "name" : client_name,
    "ip" : ip_addr,
    "UDP_port" : udp_port,
    "time" : datetime.now().strftime("%H:%M:%S")
}

info_sending = json.dumps(info)
send(REGISTER_MSG, info_sending)

msg = get_CPU_temp() + get_disk_usage() + get_RAM_usage()
send(INFO_MSG, msg)
time.sleep(10)
msg = get_CPU_temp() + get_disk_usage() + get_RAM_usage()
send(INFO_MSG, msg)
time.sleep(10)
msg = get_CPU_temp() + get_disk_usage() + get_RAM_usage()
send(INFO_MSG, msg)
time.sleep(10)
send(INFO_MSG, msg)
send(DISCONNECT_MSG, "")

# should use socket.send(send_length + message) instead of sending 2 times
# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT))



# send("HELLO")
# send(DISCONNECT_MSG)

# def GetNTPDateTime(server):
#     try:
#         ntpDate = None
#         client2 = ntplib.NTPClient()
#         response = client2.request(server, version=3)
#         ntpDate = time.ctime(response.tx_time)
#         #print (ntpDate)
#     except Exception as e:
#         print (e)
#     if(ntpDate != None):
#         return datetime.strptime(ntpDate, "%a %b %d %H:%M:%S %Y")

# print('iz gettin')
# while True:
#     a = GetNTPDateTime('uk.pool.ntp.org')
#     if(a.hour == 10 and a.minute == 11 and a.second ==59):
#         send("Hello world!")
#         #input()
#         send("Hello everyone!")
#         #input()
#         send("The pc said Hello!!!")
#         #input()
#         send("It's time to say goodbye :(")
#         send(DISCONNECT_MSG)
#         break;
