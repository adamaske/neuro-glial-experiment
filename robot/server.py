import socket

def start_server():
    # Define host and port
    host = '10.47.20.11'  # Localhost
    port = 32000        # Arbitrary non-privileged port

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for incoming connections (1 client at a time)

    print(f"Server is listening on {host}:{port}...")

    # Accept a connection
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Communicate with the client
    while True:
        data = conn.recv(1024)  # Receive data (buffer size 1024 bytes)
        if not data:
            break
        print(f"Received from client: {data.decode()}")
        conn.sendall(data)  # Echo back the data to the client

    conn.close()  # Close the connection
    print("Connection closed.")

if __name__ == "__main__":
    start_server()
