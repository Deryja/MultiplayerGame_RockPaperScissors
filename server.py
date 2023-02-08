from os import remove
from socket import *
import _thread as thread
import time

clients = []  #For å kunne binde til flere klienter som opprettes

def broadcast(message, connection):
    """
    sends message to all clients except the client who sent the message
    """
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def play_game(connection1, connection2): #Logikken til spillet

    #The logic of the game, and connects two clients to play the game together

    while True:
        connection1.send("Your turn, choose 'rock', 'paper' or 'scissors'".encode())
        choice1 = connection1.recv(1024).decode()
        connection2.send("Your turn, choose 'rock', 'paper' or 'scissors'".encode())
        choice2 = connection2.recv(1024).decode()

        if choice1 == "rock" and choice2 == "scissors":
            winner = connection1
            loser = connection2
        elif choice1 == "scissors" and choice2 == "paper":
            winner = connection1
            loser = connection2
        elif choice1 == "paper" and choice2 == "rock":
            winner = connection1
            loser = connection2
        elif choice2 == "rock" and choice1 == "scissors":
            winner = connection2
            loser = connection1
        elif choice2 == "scissors" and choice1 == "paper":
            winner = connection2
            loser = connection1
        elif choice2 == "paper" and choice1 == "rock":
            winner = connection2
            loser = connection1
        else:
            winner = None
            loser = None
        if winner:
            winner.send("You win!".encode())
            loser.send("You lose!".encode())
        else:
            connection1.send("Draw!".encode())
            connection2.send("Draw!".encode())

        response = connection1.recv(1024).decode()
        if response == "exit":
            break
        response = connection2.recv(1024).decode()
        if response == "exit":
            break

def handle_client(connection, address):

    #Function for handling the clients and connecting them to the server

    global clients
    print(f"Accepted connection from {address}")
    broadcast(f"{address} joined the chat\n".encode(), connection)
    clients.append(connection)
    while True:
        try:
            message = connection.recv(1024).decode()
            if message == "play game":
                for client in clients:
                    if client != connection:
                        client.send("Do you want to play a game with this client? (yes/no)\n".encode())
                        response = client.recv(1024).decode()
                        if response == "yes":
                            play_game(connection, client)
                            break
            else:
                broadcast(f"{address}: {message}\n".encode(), connection)
        except:
            broadcast(f"{address} left the chat\n".encode(), connection)
            print(f"Closed connection from {address}")
            connection.close()
            clients.remove(connection)
            break

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12100
    ADDRESS = (host, port)
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(5)
    print("Waiting for connection...")
    while True:
        connection, address = server.accept()
        thread.start_new_thread(handle_client, (connection, address))
    server.close()
