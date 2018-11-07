import socket
import sys
#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Pass Argument in command line including the Public IP of the server
server_address = (sys.argv[1], 10000)
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
s.bind(server_address)

s.listen(1)
conn, addr = s.accept()

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print (data.decode('utf-8'))
    
conn.close()
