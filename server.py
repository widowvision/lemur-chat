
#serverlemurchat.py

import socket
import threading
import ssl
import random

# Function to generate a unique identifier for a client
def generate_unique_id(name):
    return f"{random.randint(1000, 9999)}-{name}"

def handle_client(client_socket, addr, clients, client_names):
    # Generate a unique identifier for the client
    client_id = generate_unique_id(addr[0])
    clients[client_id] = client_socket
    client_names[client_socket] = client_id

    # Send the list of connected clients to the new client
    client_list = ', '.join(clients.keys())
    client_socket.send(f'Connected clients: {client_list}'.encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # Client disconnected, handle it
                break

            if message == 'exit':
                # Handle the 'exit' message specifically
                print(f"{client_names[client_socket]} has disconnected.")
                break

            # Split the message for a regular chat message
            try:
                target_id, msg = message.split(':', 1)
                if target_id in clients:
                    clients[target_id].send(f'[{client_id}]: {msg}'.encode('utf-8'))
                else:
                    print(f"Message target {target_id} not found.")
            except ValueError:
                print(f"Incorrect message format from {client_id}: {message}")

        except Exception as e:
            print(f"An error occurred with {client_id}: {e}")
            break

    # Clean up after disconnection
    client_socket.close()
    del clients[client_id]
    del client_names[client_socket]
    print(f"{client_id} connection closed.")


def main():
    host = 'localhost'
    port = 1080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    # Wrap the server socket with SSL for encryption
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/Users/emmahofer/Desktop/mykeys/mycertificate.crt', '/Users/emmahofer/Desktop/mykeys/mykey.key')
    secure_socket = context.wrap_socket(server_socket, server_side=True)

    print('Server is listening...')

    clients = {}
    client_names = {}

    while True:
        client_socket, addr = secure_socket.accept()
        print(f'Connected with {addr}')

        # Start a new thread for the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients, client_names))
        client_thread.start()

if __name__ == '__main__':
    main()
