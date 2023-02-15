"""
Server side: it simultaneously handle multiple clients
and broadcast when a client new client joins or a client
sends a message.
"""
from socket import *
import _thread as thread
import time
import sys

# this is too keep all the newly joined connections!
all_client_connections = []

def now():
    #returns the time of day
    return time.ctime(time.time())

def handleClient(connection, addr):
    #a client handler function 
    
    # this is where we broadcast everyone that a new client has joined
    all_client_connections.append(connection, addr)

    # append this this to the list for broadcast
    newUserMessage = f"{addr} has joined the server"            # String that tells other users that another user has joined
    broadcast(connection, newUserMessage)
    # create a message to inform all other clients
    # that a new client has just joined.
    
    
    while True:
        message = connection.recv(2048).decode()
        print(now() + " " + str(addr) + "#  ", message)
        if (message.strip() in ["quit", "exit", "escape", "esc", "out"] or not message): 
            connection.close()
            all_client_connections.remove(connection)
            broadcast(connection, f"{addr} has left the server")
            break
        # broadcast this message to the others
        else:
            broadcast(connection, f"{addr}: {message}")


def broadcast(connection, message):

    print("Broadcasting")
    for c in all_client_connections:
        if c != connection:
            try:
                c.send(message.encode())
            except:
                print ("Something went wrong!, couldn't send message to client")
                c.close()
                all_client_connections.remove(c)

def main():

    """
    creates a server socket, listens for new connections,
    and spawns a new thread whenever a new connection join
    """
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('', serverPort))     # tuple containing ip address and port number
        # The ip address is represented with '' which means that the server will bind to all available networks on the local machine    

    except:
        print("Bind failed. Error : ")
        sys.exit()
    serverSocket.listen(10)
    print('The server is ready to receive')
    while True:
        connectionSocket, addr = serverSocket.accept()

        print('Server connected by ', addr)
        print('at ', now())
        thread.start_new_thread(handleClient, (connectionSocket, addr))

    serverSocket.close()

if __name__ == '__main__':
    main()
