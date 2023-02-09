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

def handleClient(connection):     #Function that handles each client connection
    while True:
        #Username
        data = connection.recv(1024).decode()
        if not data:
            break
        print("received message = ", data)
    
        modified_message = data.upper()
        connection.send(modified_message.encode())
        
        if(data == "exit"):
            break

    connection.close()
    print('Connection closed with ', connection)
"""
handleClient(connection) is the function that handles each client connection. It reads data from the client using 
connection.recv(1024) (the 1024 specifies the maximum number of bytes to be received at once), converts the received 
bytes to a string using .decode(), and then sends back the modified data (converted to uppercase) using connection.
send(modified_message.encode()). If the client sends the message "exit", the function breaks out of the while loop and 
closes the connection using connection.close().
"""

def play_rps():
    while True:
        #Ask the user if the want to play
        userChoice = input("Do you want to play a game of rock, paper or scissors? (y/n)").lower()

        #If the answer is no, quit
        if userChoice == "n":
            print("Thanks for playing!")
            break

        if userChoice == "y":
            userChoice = input("rock, paper, scissors, shoot! (rock/paper/scissors)").lower()
            computerChoice = random.choice(["rock", "paper", "scissors"])
            print(f"you chose {userChoice} and the computer chose {computerChoice}.")

            if userChoice == computerChoice:
                print("It's a tie!")
            elif userChoice == "rock" and computerChoice == "scissors":
                print("You win!")
            elif userChoice == "paper" and computerChoice == "rock":
                print("You win!")
            elif userChoice == "scissors" and computerChoice == "paper":
                print("You win!")
            else:
                print("You lose.")

def broadcast(connectionSocket, message):
    for client in clients:
        if client != connectionSocket:
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
        broadcast(serverSocket, "A new client has joined \n")
        thread.start_new_thread(handleClient, (connectionSocket,))
    
    serverSocket.close()

if __name__ == '__main__':
    main()