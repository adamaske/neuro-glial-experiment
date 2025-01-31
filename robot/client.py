import socket

def start_client():
    # Define server host and port
    host = '10.47.20.11'  # Localhost
    port = 32000        # Same port as the server

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connected to server at {host}:{port}")

    # Communicate with the server
    try:
        while True:
            message = input("Enter message to send (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())  # Send data
            data = client_socket.recv(1024)  # Receive response
            print(f"Received from server: {data.decode()}")
    finally:
        client_socket.close()  # Close the connection
        print("Connection closed.")

if __name__ == "__main__":
    start_client()
