#clientlemurchat.py

import socket
import ssl

def main():
    host = 'localhost'
    port = 1080

    #creates client side socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # this is where the encrytion occurs, in the secure_socket
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    secure_socket = context.wrap_socket(client_socket, server_hostname=host)

    # connects using the secure socket
    secure_socket.connect((host, port))

    # displays client list
    client_list = secure_socket.recv(1024).decode('utf-8')
    print(client_list)

    while True:
        # continue typing or disconnect
        message = input("Enter message in format 'target_id:message' or 'exit' to disconnect: ")
        if message == 'exit':
            # option to disconnect
            secure_socket.send(message.encode('utf-8'))
            break
        else:
            # continue sending messages
            secure_socket.send(message.encode('utf-8'))

    secure_socket.close()

if __name__ == '__main__':
    main()
