import socket

def start_tcp_server(host='0.0.0.0', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    print(f"Server started at {host}:{port}")
    server_socket.listen(5)
    print("Waiting for a connection...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received from client: {data.decode('utf-8')}")
                response = f"Server received: {data.decode('utf-8')}"
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {client_address} closed.")

if __name__ == "__main__":
    start_tcp_server(host='10.47.15.132', port=50004)  # Replace with Computer 1's IP
