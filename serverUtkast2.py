import random
from socket import *
import _thread as thread
import time

def now():
    return time.ctime(time.time())

clients = []

def handleClient(connection, address):
    username = connection.recv(1024).decode()
    print(f'{username} ({address}) has joined the server at {now()}')
    broadcast(f'{username} ({address}) has joined the server')

    while True:
        data = connection.recv(1024).decode()
        if not data:
            break
        broadcast(f'{username}: {data}', connection)
        
        if data == 'exit':
            break

    connection.close()
    clients.remove(connection)
    print(f'{username} ({address}) has left the server at {now()}')
    broadcast(f'{username} ({address}) has left the server')


def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:
            client.send(message.encode())


def game(client1, client2):
    while True:
        client1.send(b'Enter rock, paper, or scissors: ')
        client2.send(b'Enter rock, paper, or scissors: ')
        move1 = client1.recv(1024).decode().strip().lower()
        move2 = client2.recv(1024).decode().strip().lower()
        
        if move1 == 'exit' or move2 == 'exit':
            break
        
        if move1 == move2:
            client1.send(b'Tie!')
            client2.send(b'Tie!')
        elif move1 == 'rock' and move2 == 'scissors':
            client1.send(b'You win!')
            client2.send(b'You lose!')
        elif move1 == 'paper' and move2 == 'rock':
            client1.send(b'You win!')
            client2.send(b'You lose!')
        elif move1 == 'scissors' and move2 == 'paper':
            client1.send(b'You win!')
            client2.send(b'You lose!')
        else:
            client1.send(b'You lose!')
            client2.send(b'You win!')


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', 12000))
    server_socket.listen(5)
    print(f'Server is ready to receive at {now()}')
    
    while True:
        connection_socket, address = server_socket.accept()
        clients.append(connection_socket)
        print(f'Accepted connection from {address}')
        thread.start_new_thread(handleClient, (connection_socket, address))

        if len(clients) >= 2:
            client1, client2 = clients[-2:]
            thread.start_new_thread(game, (client1, client2))

    server_socket.close()


if __name__ == '__main__':
    main()