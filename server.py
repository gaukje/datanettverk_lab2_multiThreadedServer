"""
The other side must be passive
☞ it is prepared for accepting connections
☞ waits for someone else to take initiative for creating a connection
☞ this side is called the server
"""
from socket import *
import _thread as thread
import time

def now():
    #Returns the time of day
    return time.ctime(time.time())

def handleClient(connection):
    #Client handler
    while True:
        data = connection.recv(1024).decode()
        
        print("received message = ", data)
        
        modified_message = data.upper()
        connection.send(modified_message.encode())
        
        if(data == "exit"):
            break

        connection.close()


def main():
    #Creates a server cocket, listens for new connections and spawns a new thread for new connections

    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)

    try:
        serverSocket.bind('',serverPort)
    
    except: 
        print("Bind failed. Error :" )

    serverSocket.listen(1)
    print ('The server is ready to receive')

    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Server connected by ', addr)
        print('at ', now())
        thread.start_new_thread(handleClient, (connectionSocket,))
    serverSocket.close()

if __name__ == '__main__':
    main()