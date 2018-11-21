"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s!' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    print(msg)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
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

        
clients = {}
addresses = {}

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
    
    
    
