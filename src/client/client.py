from os import system
from datetime import datetime
import socket
import ntplib
import time
import psutil
import pickle
import json
import ipaddress
import platform
# import netifaces
import threading
# import subprocess
import sys



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
CMD = 5

FORMAT = 'utf-8'
SEND_PORT = 0
INTERVAL = 10
DISCONNECT_MSG = "!DISC"
REGISTER_MSG = "!RGTR"
INFO_MSG = "!INFO"
SUCCEEDED_MSG = "!SUCC"
FAILED_MSG = "!FAIL"
UPDATE_MSG = "!UPDT"

reg_succeeded = False
exiting = False
exit_confirmed = False
server_unavailable = False
packet_length = 1024

info = {}

opened = False

# METHOD IMPLEMENTATION
# Getting server's ip address through input (since we find the ip address of dynamically)
def ipEntered():
    while True:
        try:
            val = input("Please enter the ip address of the server you wish to connect with: ")
            return ipaddress.ip_address(val)
        except ValueError:
            print("Not a valid IP address")

# this is hardcoded (no good), will find ways to code it better afterward
def get_CPU_temp():
    global opened

    if (platform.system() == 'Darwin'):
        return "A temperature value"
    if (platform.system() == 'Linux'):
        return f"CPU temperature: {psutil.sensors_temperatures()['cpu_thermal'][0].current}\n"
    if (platform.system() == 'Windows'):
        import wmi
        if not opened:
            subprocess.Popen('OpenHardwareMonitor.exe', shell=True)
            time.sleep(5)
            opened = True
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType==u'Temperature':
                if (sensor.Name == 'CPU Package'):
                    return f"{sensor.Name}'s temp: {sensor.Value}\n"

def get_cpu_percent():
    return f"Average CPU % used: {psutil.cpu_percent()}\n"

def get_disk_usage():
    return f"Storage % used: {psutil.disk_usage('/')[3]}\n"

def get_RAM_usage():
    return f"Memory % used: {psutil.virtual_memory()[2]}\n"

def send(cmd, msg):
    global reg_succeeded
    global INTERVAL
    global info 
    global exiting
    global server_unavailable
    global exit_confirmed

    message = (cmd + msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    try:
        client_send.send(send_length + message)
    except:
        print(f"Cannot send msg to server. Type EXIT to end the program")
        server_unavailable = True
        return

    if cmd == REGISTER_MSG:
        try:
            raw_msg = client_send.recv(packet_length)
            msg_length = raw_msg[0:HEADER].decode(FORMAT) # first 16 bytes
            if msg_length:
                try:
                    msg_length = int(msg_length)
                    print(f"The length of the msg: {msg_length}")
                    cmd = raw_msg[HEADER:HEADER+CMD].decode(FORMAT)
                    print(f"The type of the msg: {cmd}")
                    if cmd == SUCCEEDED_MSG:
                        msg = raw_msg[HEADER+CMD:].decode(FORMAT)
                        info = json.loads(msg)
                        print(info["client_id"])
                        print(info["tcp_port"])
                        print(info["interval"])
                        INTERVAL = info["interval"]
                        reg_succeeded = True
                except ValueError:
                    print(f"The message length is not recognizable! Abort the message")
                    reg_succeded = False
        except Exception as e:
            print(e)
            print(f"Cannot listen from server. Type EXIT to end the program")
            server_unavailable = True
            return

    if cmd == INFO_MSG and reg_succeeded:
        # Handle this later
        try:
            confirmation = client_send.recv(packet_length).decode(FORMAT)
            print(confirmation)
        except: 
            print(f"Cannot listen from server. Type EXIT to end the program")
            server_unavailable = True
            return
            

    if cmd == DISCONNECT_MSG and reg_succeeded:
        # Handle this later
        try:
            confirmation = client_send.recv(packet_length).decode(FORMAT)
            exit_confirmed = True
            print(confirmation)
        except: 
            print(f"Cannot listen from server. Type EXIT to end the program")
            server_unavailable = True
            return
        

#=====================================================

SERVER = str(ipEntered())
TCP_PORT = 34567 # to send the register info
ADDR = (SERVER, TCP_PORT)

# Sending 
client_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_send.connect(ADDR)
except Exception as e:
    print(e)
    print("Can't connect to server. Exiting...")
    sys.exit()


# Receiving
client_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_name = socket.gethostname()

ip_addr = ""
def findIP():
    global ip_addr
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
findIP()
client_recv.bind((ip_addr, 0))
udp_port = client_recv.getsockname()[1]

info = {
    "name" : client_name,
    "ip" : ip_addr,
    "UDP_port" : udp_port,
    "time" : datetime.now().strftime("%H:%M:%S")
}

info_msg = json.dumps(info)
while not reg_succeeded:
    send(REGISTER_MSG, info_msg)

def info_sending():
    global exiting

    while not exiting:
        t_end = time.time() + INTERVAL
        while time.time() < t_end:
            if exiting:
                return
            # wait
        msg = get_cpu_percent() + get_disk_usage() + get_RAM_usage()
        send(INFO_MSG, msg)

    # while not exiting:
    #     msg = get_cpu_percent() + get_disk_usage() + get_RAM_usage()
    #     send(INFO_MSG, msg)
    #     time.sleep(INTERVAL)
    
        

def update_listening():
    global INTERVAL
    global exiting

    while not exiting:
        try:
            data, addr = client_recv.recvfrom(1024)
        except:
            print("UDP port is now unavailable. Exiting...")
            break
        msg_length = data[0:HEADER].decode(FORMAT) # first 16 bytes
        if(msg_length):
            try:
                msg_length = int(msg_length)
                print(f"The length of the msg: {msg_length}")
                cmd = data[HEADER:HEADER+CMD].decode(FORMAT)
                print(f"The type of the msg: {cmd}")
                msg = data[HEADER+CMD:].decode(FORMAT)
                # need to check the validity
                try:
                    interval = int(msg)
                    INTERVAL = interval
                    info["interval"] = INTERVAL
                    print(f"INTERVAL changed to: {INTERVAL}")
                except ValueError:
                    print(f"The data is not integer") 
            except ValueError:
                print(f"The length is not recognizable! Abort the message.")

def input_command():
    global exiting
    global server_unavailable
    global exit_confirmed

    while not exiting:
        command = input()
        if (command == "EXIT"):
            exiting = True
            client_recv.close()
            if not server_unavailable:
                print("DISCONNECTING:")
                send(DISCONNECT_MSG, "")
                t_end = time.time() + INTERVAL
                while time.time() < t_end:
                    if (exit_confirmed):
                        print("DISCONNECTED!")
                        return

if reg_succeeded:
    thread_listening = threading.Thread(target=update_listening)
    thread_sending = threading.Thread(target=info_sending)
    thread_command = threading.Thread(target=input_command)
    thread_listening.start()
    thread_sending.start()
    thread_command.start()




# msg = get_CPU_temp() + get_disk_usage() + get_RAM_usage()
# send(INFO_MSG, msg)
# time.sleep(INTERVAL)
# msg = get_CPU_temp() + get_disk_usage() + get_RAM_usage()
# send(INFO_MSG, msg)
# time.sleep(INTERVAL)
# msg = get_CPU_temp() + get_disk_usage() + get_RAM_usage()
# send(INFO_MSG, msg)
# time.sleep(INTERVAL)
# send(INFO_MSG, msg)
# send(DISCONNECT_MSG, "")

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
