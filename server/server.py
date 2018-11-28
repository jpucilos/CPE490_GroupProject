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
        client.send(bytes("Then, please type in a group name, use general for everyone\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    while True:
            if(client.recv(BUFSIZ).decode("utf8") == "E394"): #verification code from client
                name = client.recv(BUFSIZ).decode("utf8")
                group = client.recv(BUFSIZ).decode("utf8")
                welcome = 'Welcome %s!\n' % name
                client.send(bytes(welcome, "utf8"))
                intro = "%s has joined the chat!" % name
                print(intro)
                broadcast(bytes(intro, "utf8"))
                clients[client] = name
                groups[client] = group
                print(groups)
                break

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
                if ((msg == bytes("E394", "utf8")) & (len(ver) != 0)):
                        cli=ver.pop()
                        cli.send(bytes("Message received\n", "utf8"))
                elif ((msg != bytes("E394","utf8")) & (len(ver) == 0)):
                        cast(client, msg, name+": ")
                        ver.append(client)
        else:
                #client.send(bytes("{quit}", "utf8"))
                client.close()
                close_annoucement = name + " has left the chat."
                print (close_annoucement)
                del clients[client]
                broadcast(bytes(close_annoucement, "utf8"))
                break


def cast(sender, msg, prefix=""):  # prefix is for name identification.
        if(groups[sender] == "general"):
                broadcast(msg, prefix) #send to all
        else:
                for sock in groups:
                        if(groups[sock] == groups[sender]): #find people in that group and send to them
                                sock.send(bytes(prefix, "utf8")+msg+bytes("\n", "utf8"))


def broadcast(msg, prefix=""):
        for sock in clients:
                sock.send(bytes(prefix, "utf8")+msg+bytes("\n", "utf8"))


clients = {}
addresses = {}
groups = {}
ver=[]

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
