#clientlemurchat.py

import socket
import ssl

def main():
    host = 'localhost'
    port = 1080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the client socket with SSL for encryption
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    secure_socket = context.wrap_socket(client_socket, server_hostname=host)

    secure_socket.connect((host, port))

    # Receive and print the list of connected clients
    client_list = secure_socket.recv(1024).decode('utf-8')
    print(client_list)

    while True:
        # Prompt the user to enter a message or type 'exit' to disconnect
        message = input("Enter message in format 'target_id:message' or 'exit' to disconnect: ")
        if message == 'exit':
            # Send the "exit" message to the server to disconnect
            secure_socket.send(message.encode('utf-8'))
            break
        else:
            # Send a message using the target client's unique identifier
            secure_socket.send(message.encode('utf-8'))

    secure_socket.close()

if __name__ == '__main__':
    main()
