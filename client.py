import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Replace with server's IP and port if necessary

    while True:
        # Prompt the user to enter a message or type 'exit' to disconnect
        message = input("Enter message or 'exit' to disconnect: ")
        if message == 'exit':
            # Send the "exit" message to the server to disconnect
            client_socket.send(message.encode('utf-8'))
            break
        else:
            # Client A wants to send a message to another client (like Client B)
            pass

            # Send a message using Client B's unique identifier (placeholder)
            client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == '__main__':
    main()
