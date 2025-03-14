import socket

def tcp_client(host, port, message):
    """
    A simple TCP client.

    Args:
        host (str): The hostname or IP address of the server.
        port (int): The port number of the server.
        message (str): The message to send to the server.
    """
    try:
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))

        # Send the message
        client_socket.send(message.encode('utf-8'))

        # Receive the response (optional)
        data = client_socket.recv(1024) #receive up to 1024 bytes
        print(f"Received from server: {data.decode('utf-8')}")

    except ConnectionRefusedError:
         print(f"Connection refused. Server at {host}:{port} may not be running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        if 'client_socket' in locals(): #check if socket was created to avoid error if connection failed before creation.
            client_socket.close()

if __name__ == "__main__":
    host = "192.168.0.101"  # Replace with the server's IP address or hostname
    port = 32000        # Replace with the server's port number

    message = "Hello, server!"

    tcp_client(host, port, message)