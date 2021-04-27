


# About

Assignment 1 of computer networking's implementation

# Task list
- Protocol defining
- Implementing the server and client with the defined protocol.
- ~~Dynamically geting the server's IP~~. (Currently using the hackish way, will test it with another computer tmr).
    > This works (kind of).
- ~~Find way to listen udp port on client.~~
- Update the interval time by sending udp packet        
    >(Only 2 clients on the same host is okay, but sending the udp packet through the subnet (aka sending it to another client in the subnet) seems not working)
    > Gotta finds way to fix this asap
    > Update: Somehow manage to change the inverval by sending UDP packet to the MACOSX device, gotta know what the cause is then.
- ~~Change the interval time on client and track it~~ (Still only 1 client).
- ERROR HANDLING!!!
- Multiple clients handling on server.
- Compile it into a independent program.
- ~~Including Open Hardware Monitor when running the server.~~
    > Such a burden to handle, not recommend using OpenHardwareMonitor anymore, gonna find another way
- Find alternative ways to get temperature info without using Open Hardware Monitor.
    > Must do must do!
- Scenarios' definition.
- (optional) GUI
- Find ways to disconnect the client properly.
