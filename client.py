#clientlemurchat.py
import socket
import ssl
import threading

def listen_for_messages(secure_socket):
    while True:
        try:
            incoming_message = secure_socket.recv(1024).decode('utf-8')
            if incoming_message:
                print(incoming_message)
        except OSError as e:
            if e.errno == 9:  # Bad file descriptor
                print("\nConnection closed.")
                break
            else:
                raise

def main():
    host = 'localhost'
    port = 1080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the client socket with SSL for encryption
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    secure_socket = context.wrap_socket(client_socket, server_hostname=host)

    secure_socket.connect((host, port))

    username = input("Enter your username: ")
    secure_socket.send(username.encode('utf-8'))

    threading.Thread(target=listen_for_messages, args=(secure_socket,)).start()

    try:
        while True:
            message = input("\nEnter message or 'exit' to disconnect: ")
            if message == 'exit':
                secure_socket.send(message.encode('utf-8'))
                break
            else:
                # Broadcast message to all clients
                secure_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        secure_socket.close()

if __name__ == '__main__':
    main()

