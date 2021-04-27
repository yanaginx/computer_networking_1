import socket
import select

s = socket.socket()
s.bind(('',8000))
s.listen(1)

readable = [s] # list of readable sockets.  s is readable if a client is waiting.
i = 0
while True:
    # r will be a list of sockets with readable data
    r,w,e = select.select(readable,[],[],0)
    for rs in r: # iterate through readable sockets
        if rs is s: # is it the server
            c,a = s.accept()
            print('\r{}:'.format(a),'connected')
            readable.append(c) # add the client
        else:
            # read from a client
            data = rs.recv(1024)
            if not data:
                print('\r{}:'.format(rs.getpeername()),'disconnected')
                readable.remove(rs)
                rs.close()
            else:
                print('\r{}:'.format(rs.getpeername()),data)
    # a simple spinner to show activity
    i += 1
    print('/-\|'[i%4]+'\r',end='',flush=True)