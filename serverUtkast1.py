"""
The other side must be passive
☞ it is prepared for accepting connections
☞ waits for someone else to take initiative for creating a connection
☞ this side is called the server
"""
import random
from socket import *
import _thread as thread #The import _thread as thread statement imports the thread module as thread, which provides a way to run multiple threads (also known as light-weight processes) in parallel within a single process.
import time

def now():
    #Returns the time of day
    return time.ctime(time.time())

clients = []
client_count = 0

def handleClient(connection):     #Function that handles each client connection
    
    global client_count
    client_count += 1

    #Username
    username = connection.recv(1024).decode()
    print(f'{username} joined the server \n')
    clients.append(connection)
    connection.send(f'{username}, you have the joined the chat \n'.encode())
    broadcast(connection, f'{username} joined the chat')
    
    while True:    
        data = connection.recv(1024).decode()
        if not data:
            break
        print("received message from {username} : {data} ")
        broadcast(f"{username}: {data}", connection)
        
        if(data == "exit"):
            break
    
    clients.remove(connection)
    client_count -= 1
    broadcast(f"{username} has left the chat", connection)
    connection.close()
    print(f'Connection closed with {username} ')


def broadcast(message, sender):
    for client in clients:
        if client != client:
            client.send(message.encode())


def main():
    #Creates a server socket, listens for new connections and spawns a new thread for new connections

    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('',serverPort))
    except: 
        print("Bind failed. Error :" )
    serverSocket.listen(5)
    print ('The server is ready to receive')
    #play_rps()

    connectedClients = [serverSocket]

    while True:
        connectionSocket, addr = serverSocket.accept()
        connectedClients.append(connectionSocket)
        print('Server connected by ', addr)
        print('at ', now())
        broadcast(serverSocket, "A new client has joined ".lower())
        thread.start_new_thread(handleClient, (connectionSocket,))
    
    serverSocket.close()

if __name__ == '__main__':
    main()