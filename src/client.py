import socket
from datetime import datetime
import ntplib
import time
"""
The protocol:
Client: 
    Send its registering information through TCP, including its Name, IP addr, UDP port (to recieve server's info), current date/time 

Registering packet: "!REGISTER + info"


// Considering using pickle on packing the data
"""


HEADER = 64
PORT = 34567
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
# SERVER = "172.29.128.1"
SERVER = "192.168.43.134"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# should use socket.send(send_length + message) instead of sending 2 times
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello world!")
send(DISCONNECT_MSG)

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
