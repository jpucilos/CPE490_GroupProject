import socket
import sys
from threading import thread

#TO be replaced with Data from MongoDB possibly?
clients = {}
addresses = {}

#Pass Argument in command line including the Public IP of the server
server_address = (sys.argv[1], 10000)
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)


def listen_for_clients():
	#Infinite loop that's always looking for new clients to enter the chatroom
	while True:
		conn, addr = s.accept()
		print ("A new member has joined the room")
		conn.send(bytes("Welcome to the room! Type your name and press enter!", "utf-8")
		addresses[conn] = addr
		Thread(target=handle_client, args= (conn,)).start()
		
def handle_client(conn):
	#handles client after person joins
	name = conn.recv(BUFFER_SIZE).decode("utf-8")
	welcome = "Welcome " + name + ", if you want to quit, type 'quit' to exit"
	conn.send(bytes(welcome, "utf-8")
	msg = name + " has joined the chat!"
	broadcast(bytes(msg, "utf-8"))
	clients[conn] = name
	while True:
		msg = conn.recv(BUFFER_SIZE).decode("utf-8")
		if msg != "quit"
			broadcast(bytes(name + ": " + msg, "utf-8"))
		else:
			conn.close()
			del clients[conn]
			broadcast(bytes(name + " has left the room")
			break
	return

def broadcast(message)
	#Broadcast to group
	for sock in clients:
		sock.send(message)
	return


s.listen(5)
print("Waiting Connection....")
accept_thread = Thread(target = listen_for_clients)
accept_thread.start()
accept_thread.join()

#Server closes when both of the processes above close
s.close()
