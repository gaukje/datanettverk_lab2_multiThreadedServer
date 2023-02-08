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