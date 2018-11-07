import socket
import sys
#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Pass Argument in command line including the Public IP of the server
server_address = (sys.argv[1], 10000)
s.connect(server_address)

try:

    while True:
        message = input("Enter Message, or type 'q' to Quit:")
        if (message == 'q'): break
        else:
            s.sendall(message.encode('utf-8'))
finally:
    s.close()

