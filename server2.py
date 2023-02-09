import socket

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(10)

    print("Server is ready to receive connections...")

    while True:
    client_socket, client_address = server_socket.accept()
    print("Received connection from {}".format(client_address))
    clients.append(client_socket)
    broadcast("{} joined the chat".format(client_address), client_socket)
    
    while True:
        message = client_socket.recv(1024).decode("utf-8")
        if message:
            broadcast(message, client_socket)
        else:
            client_socket.close()
            clients.remove(client_socket)
            broadcast("{} left the chat".format(client_address), client_socket)
            break
def main():
    # initialize server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((127.0.0.1, 12000))
    server_socket.listen(5)
    print(f"Server started at {127.0.0.1}:{12000}")

    # initialize list to store connected clients
    clients = []

    while True:
        # wait for new clients to connect
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # add new client to the list of connected clients
        clients.append(client_socket)

        # notify other clients of the new client's arrival
        broadcast(client_socket, " joined the chat!", clients)

        # start a new thread to handle communication with the new client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients))
        client_thread.start()

if __name__ == "__main__":
    main()  


"""
            In the above code, clients is a list that keeps track of all the connected clients. The broadcast function takes a message and sender socket as input and sends the message to all clients except the sender. The server_socket is created and bound to the IP address 0.0.0.0 and port 5000. The server is then set to listen for incoming connections.

The main loop accepts incoming connections and adds the client socket to the clients list. The broadcast function is called to notify all clients that a new client has joined the chat.

Another loop is started to receive messages from the client. The recv method is used to receive messages and the send method is used to broadcast the messages to all clients except the sender. If a client disconnects, the client socket is closed, removed from the clients list and a broadcast is sent to notify all clients that the client has left the chat.
            """