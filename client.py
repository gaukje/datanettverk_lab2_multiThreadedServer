from socket import *
import sys
import select
# Client side connects to the server and sends a message to everyone

server_ip = "127.0.0.1" #Standard IP adress
server_port = 12000 #Standard port
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_ip, server_port))


while True:
    """ we are going to use a select-based approach here because it will help
    us deal with two inputs (user's input (stdin) and server's messages from 
    socket)
    """
    inputs = [sys.stdin, client_socket]

    print(inputs)

    """ read the select documentations - You pass select three lists: the 
    first contains all sockets that you might want to try reading; the 
    second all the sockets you might want to try writing to, and the last 
    (normally left empty) those that you want to check for errors. """

    read_sockets, write_socket, error_socket = select.select(inputs, [], [])
    # we check if the message is either coming from your terminal or
    # from a server
    for socks in read_sockets:
        if socks == client_socket:
            try:
                message = socks.recv(2048).decode()
                print(message)
                # receive message from client and display it on the server side
                # exception if there is no message
                if not message:
                    print("Connection closed by server")
                    # exit if there is no message
                    sys.exit
                elif "has left" in message:
                    print(message)
                    pass
                print("Message from server: ", message)
            except Exception as e:
                print("Error receiving message from server", e)
        else:
            # takes inputs from the user
            message = sys.stdin.readline()
            # send a message to the server
            client_socket.send(message.encode())
            """
            if message.strip() in ["quit", "exit", "escape", "esc", "out"]:
                client_socket.close()
                sys.exit()
                """
client_socket.close()