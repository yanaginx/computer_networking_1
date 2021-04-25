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
        - When sending the change in interval time, if within 5s the server doesn't receive the received change message from the client then the server will resend the change.

### Clean disconnection:
    Sent the message "!DISC" to confirm clients' disconnection.        

#### Msg format: 
    [msg's length] + [5 bytes command abbriviation] + [data]
#### Registering packet: 
    "!RGTR + [info]"
#### Succeeeded register confirmation packet:
    "!SUCC + [info]"
#### Failed register confirmation packet:
    "!FAIL + [info]"
#### Info package packet: 
    "!INFO + [info]"
#### Info package receive confirmation:
    "!INFO: RECEIVED"

#### Disconnecting packet:
    "!DISC"
#### Disconnection package receive confirmation:
    "!DISC: RECEIVED"    

#### Change message (server side)
    "!UPDT + [change]"
#### Change message confirmation (client will send this)
    "!UDPT: RECEIVED"



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