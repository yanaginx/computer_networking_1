## [0.0.12] - Apr 29th 2021
### Updated
  - Updated report

## [0.0.11] - Apr 29th 2021
### Updated
  - Updated `client`'s exit command, now we don't have to wait for the end of interval.
  - Updated `server`'s error handlings.
  - Updated `client`'s error handlings. 
## [0.0.10] - Apr 28th 2021
### Updated
  - Updated `client`'s id generator.
  - Handling error on receiving confirmation from `server` (`!INFO`, `!RGTR` and `!DISC`).
  - Remove `client` from `server`'s `client_info` dict when `client` disconnected.
  - Update `server` handling on `json` format.
## [0.0.9] - Apr 27th 2021
### Updated
  - Updated client and server error handling:
    - The client's disconnection: The user type `EXIT` command it will wait until the end of the `INTERVAL` time.
    - The server's sudden disconnection: the client will be prompt to exit the program to make a new connection.
    - Handling on server's confirmation sending on `!INFO` and `!RGTR`.
  - Change the CPU's temperature to CPU's utilization on client.
### Added
  - A server reference on using `select()` (not yet tested).

## [0.0.8] - Apr 27th 2021
### Updated
  - Updated client's temperature for MACOSX device
  - Updated Task lists in `README.md` 
  - Updated Protocol in `PROTOCOL.md` (Adding scenario and error handling cases) 
    >Only prototype, will complete it later.
    
## [0.0.7] - Apr 27th 2021
### Updated
  - Updated `README.md` for task lists progress.
### Added
  - The OpenHardwareMonitor's bundles to somehow get the CPU's temperature.
## [0.0.6] - Apr 26th 2021
### Updated
  - Updated the client's listening function, the client can now change his interval by listening to server's update message.
  - Updated the way to get server's IP dynamically.
  - The keyboard interrupt on client isn't working now since the listening command (recvfrom()) is blocking it.
  - Update `README.md` with bunch of task lists.
  
## [0.0.5] - Apr 25th 2021
### Updated
  - Updated the server, sending info to client when registration succeeded.
  - Updated the client's functions, sending the info until keyboard interrupt (Ctrl + C).
  - Updated the PROTOCOL (Adding more reply message on both ends).
  - Used `client.py` file on Minh's branch.

## [0.0.4] - Apr 20th 2021
### Added
  -  A new branch that has only 1 client version (gonna try to update the server for more interaction with client maybe)
### Updated
  -  Fixed a small bug in client with Python 3.5, need to install future-fstring package.

## [0.0.3] - Apr 18th 2021
### Added
  - The protocol's definition
  - Client's side scripts specified for Windows (`client_windows.py`) and Linux distros (`client_linux.py`).
### Updated
  - Simple implementation of client and server on the defined protocol.
  > To do list: <br>
  -- Find ways to handle multiple connections (and addressing them) <br>.
  -- Find ways to edit the interval times <br>

## [0.0.2] - Apr 16th 2021
### Updated
  - Simple client's computer info getting and sending to server on specified time interval, the details on how the dependencies used should be include in the `client.py` script. 
  - Simple server's handling request, the active connections isn't correctly indicated though, will find ways to fix it later

## [0.0.1] - Apr 15th 2021

### Added
  - Simple implementation of server and client (`src/server.py` and `src/client.py`)
  - Report
