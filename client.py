import sys
from socket import *

def main():

   #This is to connect to the server, reciveve broadcast messages and sends messaged to broadcast to everyone


    server_name = '127.0.0.1'
    server_port = 12100
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((server_name, server_port))
    except:
        print("ConnectionError")
        sys.exit()
    print("Connected to server\n")
    client_socket.send(("Client joined the chat\n").encode())
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(f"\n{message}")
        message = input("Enter your message: ")
        client_socket.send(message.encode())
    client_socket.close()

if __name__ == "__main__":
    main()
