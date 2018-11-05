import socket

s = socket.socket()
host = 'localhost'
port = 1247
s.connect((host, port))
print (s.recv(1024))

while True:
    inpt = input("type anything and click enter, 'q' to quit... ")
    if (inpt == 'q'):
        exit()
    else:
        s.send(str.encode(inpt))
