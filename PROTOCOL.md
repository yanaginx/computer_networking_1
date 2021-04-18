# Protocol defining

## The protocol:

### Client: 
    Send its registering information through TCP, including its Name, IP addr, UDP port (to recieve server's info), current date/time 

### Server:
        - After receiving registering information from the client, server send the unit id of client, the tcp port and the interval to the client.
        - Server can send message to the client through the udp port client sent.
        - Reply to registering packets:
            "!SUCC + [info]"
            or "!FAIL + [error]"

### Clean disconnection:
    Sent the message "!DISC" to confirm clients' disconnection.        

#### Msg format: 
    [msg's length] + [5 bytes command abbriviation] + [data]
#### Registering packet: 
    "!RGTR + [info]"
#### Info package packet: 
    "!INFO + [info]"
#### Disconnecting packet:
    "!DISC"
#### Succeeeded register confirmation packet:
    "!SUCC + [info]"
#### Failed register confirmation packet:
    "!FAIL + [info]"



#### Client's sending data:
- CPU temp, Disk drive's usage, RAM's usage
```
    CPU temp: using psutil (linux), using WMI and OpenHardwareMonitor (windows)
    Disk drive's usage: using psutil
    RAM's usage: using psutil
```
- Header (indicating the length of the data): 16 bytes
- Command abbriviate: 5 bytes 
- Length of the sending data is no longer than 235 bytes
    
> Currently working on it, if there are any changes feel free to inform me and edit the code if necessary, also please update the `CHANGELOG.md` file too!