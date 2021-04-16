import socket
from datetime import datetime
import ntplib
import time
import psutil
import pickle
import wmi


"""
Client's dependencies:
    ntplib
    psutil
    wmi
"""

"""
The protocol:
Client: 
    Send its registering information through TCP, including its Name, IP addr, UDP port (to recieve server's info), current date/time 

Registering packet: "!REGISTER + info"


// Considering using pickle on packing the data

Client's sending data:
	CPU temp, Disk drive's usage, RAM's usage
        CPU temp: using WMI and OpenHardwareMonitor
        Disk drive's usage: using psutil
        RAM's usage: 
    Header (indicating the length of the data is 16 bytes)
    Length of the sending data is no longer than 240 bytes
"""

# VARIABLE DEFINITION
HEADER = 16
PORT = 34567
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER = "192.168.0.101"
ADDR = (SERVER, PORT)

# METHOD IMPLEMENTATION
def getCPUTemp():
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
        if sensor.SensorType==u'Temperature':
            if (sensor.Name == 'CPU Package'):
                return f"{sensor.Name}'s temp: {sensor.Value}\n"

def getDiskUsage():
    return f"disk % used: {psutil.disk_usage('/')[3]}\n"

def getRAMUsage():
    return f"memory % used: {psutil.virtual_memory()[2]}\n"

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length + message)
    print(client.recv(2048).decode(FORMAT))    

#=====================================================

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

msg = getCPUTemp() + getDiskUsage() + getRAMUsage()
send(msg)
time.sleep(10)
msg = getCPUTemp() + getDiskUsage() + getRAMUsage()
send(msg)
time.sleep(10)
msg = getCPUTemp() + getDiskUsage() + getRAMUsage()
send(msg)
time.sleep(10)
send(DISCONNECT_MSG)

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