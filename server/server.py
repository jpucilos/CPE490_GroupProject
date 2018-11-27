"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import pymongo

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Hello! Type your name and press enter!\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    entry_key = ""
    if messages.find_one({"name": name}) != None:
        client.send(bytes("Please enter your entry key" , "utf8")  + bytes("\n"))
        find_password = messages.find_one({"name": name}, {"_id": 0, "entry_key": 1})
        print( find_password )
    else:
        welcome = 'Welcome %s!' % name
        client.send(bytes(welcome + " Please enter an entry key for future use.", "utf8") + bytes("\n"))
        entry_key = client.recv(BUFSIZ).decode("utf8")
        
        
        

    msg = "%s has joined the chat!" % name
    print(msg)
    broadcast(bytes(msg, "utf8"))
    messages.insert_one({"name": name, "entry_key": entry_key, "message" : msg})
    
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
            messages.insert_one({"name": name, "entry_key": entry_key, "message" : msg})
        else:
            #client.send(bytes("{quit}", "utf8"))
            client.close()
            close_annoucement = name + " has left the chat."
            print (close_annoucement)
            del clients[client]
            broadcast(bytes(close_annoucement, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg+bytes("\n"))

#Pymongo Set-up        
clients = {}
addresses = {}
myClient = pymongo.MongoClient("mongodb://localhost:27017/")
myDatabase = myClient["server_database"]
print("We made it this far")

messages = myDatabase["messages"]
	
#Socket set-up
BUFSIZ = 1024
ADDR = (sys.argv[1], 10000)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, daemon = True)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    
    
    
