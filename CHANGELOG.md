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
