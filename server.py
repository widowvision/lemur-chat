
#serverlemurchat.py

import socket
import threading
import ssl
import random

def broadcast_message(clients, message, sender_id=None):
    for client_id, client_socket in clients.items():
        if client_id != sender_id:
            try:
                client_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to {client_id}: {e}")

def handle_client(client_socket, addr, clients, client_names):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        client_id = generate_unique_id(username)
        clients[client_id] = client_socket
        client_names[client_socket] = client_id

        # Log connection with username instead of address
        print(f'\nConnected with {username}')

        client_socket.send(f'\nYou are connected with username: {username}'.encode('utf-8'))

        # Broadcast that a new user has joined
        broadcast_message(clients, f"\n{username} has joined the chat.", client_id)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            if message == 'exit':
                print(f"\n{username} has disconnected.")
                break

            broadcast_message(clients, f'[{username}]: {message}', client_id)

    except Exception as e:
        print(f"An error occurred with {username}: {e}")
    
    finally:
        # Broadcast that a user has left
        broadcast_message(clients, f"\n{username} has disconnected.", client_id)
        client_socket.close()
        del clients[client_id]
        del client_names[client_socket]
        print(f"\n{username} connection closed.")

def generate_unique_id(name):
    return f"{random.randint(1000, 9999)}-{name}"

def main():
    host = 'localhost'
    port = 1080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/Users/emmahofer/Desktop/mykeys/mycertificate.crt', '/Users/emmahofer/Desktop/mykeys/mykey.key')
    secure_socket = context.wrap_socket(server_socket, server_side=True)

    print('Server is listening...')

    clients = {}
    client_names = {}

    while True:
        client_socket, addr = secure_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients, client_names))
        client_thread.start()

if __name__ == '__main__':
    main()
