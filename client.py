"""
One side must be the active one
☞ take the initiative in creating the connection
☞ this side is called the client
"""


from socket import *
import sys
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)  #This line creates a new socket using the AF_INET address family and the SOCK_STREAM socket type. The AF_INET address family specifies that the socket is using the IPv4 protocol, and the SOCK_STREAM socket type indicates that the socket is using the TCP protocol.

try: 
    clientSocket.connect((serverName, serverPort))

except:
    print("ConnectionError")
    sys.exit()

while True:
    sentence = input('What would you like to send to the server?')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    
    print('From Server : ', modifiedSentence.decode())
    
    if(sentence == "exit"):
        break

clientSocket.close()