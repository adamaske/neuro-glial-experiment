import socket
import threading

CONTROLLER_SERVER_HOST = '192.168.3.11'
CONTROLLER_SERVER_PORT = 12345  # Choose an appropriate port
ROBOT_SERVER_HOST = '0.0.0.0'  # Listen on all available interfaces
ROBOT_SERVER_PORT = 54321  # Choose an appropriate port

controller_socket = None
robot_socket = None
robot_address = None


def handle_robot_client():
    """Handles communication with the robot client."""
    global controller_socket, robot_socket, robot_address

    try:
        while True:
            data = robot_socket.recv(1024)  # Receive data from robot
            if not data:
                print(f"Robot client {robot_address} disconnected.")
                break

            try:
                decoded_data = data.decode('utf-8')  # Decode the data
                # Add your validation logic here
                print(f"Received from robot: {decoded_data}")

                if controller_socket:
                    controller_socket.sendall(data)  # Send to controller server
                    print(f"Sent to controller: {decoded_data}")
                else:
                    print("Controller server not connected. Dropping robot data.")

            except UnicodeDecodeError:
                print("Invalid data received from robot.")
            except Exception as e:
                print(f"Error processing robot data: {e}")
                break

    except Exception as e:
        print(f"Robot client handler error: {e}")
    finally:
        if robot_socket:
            robot_socket.close()
            robot_socket = None
        print("Robot client handler stopped.")

def connect_to_controller():
    """Connects to the controller server."""
    global controller_socket

    try:
        controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        controller_socket.connect((CONTROLLER_SERVER_HOST, CONTROLLER_SERVER_PORT))
        print(f"Connected to controller server at {CONTROLLER_SERVER_HOST}:{CONTROLLER_SERVER_PORT}")

    except Exception as e:
        print(f"Failed to connect to controller server: {e}")
        controller_socket = None

def start_robot_server():
    """Starts the robot server and accepts incoming connections."""
    global robot_socket, robot_address

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ROBOT_SERVER_HOST, ROBOT_SERVER_PORT))
        server_socket.listen(1)

        print(f"Robot server listening on {ROBOT_SERVER_HOST}:{ROBOT_SERVER_PORT}")

        robot_socket, robot_address = server_socket.accept()
        print(f"Accepted connection from robot client: {robot_address}")
        robot_thread = threading.Thread(target=handle_robot_client)
        robot_thread.daemon = True  # Allow program to exit even if thread is running
        robot_thread.start()
        server_socket.close() #close the listening socket after connection is made.

    except Exception as e:
        print(f"Robot server error: {e}")
    finally:
        if server_socket:
            server_socket.close()

if __name__ == "__main__":
    connect_to_controller()
    start_robot_server()
    #The robot thread will now handle communication.
    #The main program will end after the first robot client connects.
    #For multiple robot clients, the server socket must remain open in a loop.