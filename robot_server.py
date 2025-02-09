
import socket
from pylsl import StreamInfo, StreamOutlet

ur_server_ip = "10.49.0.2"
ur_server_port = 32000
ur_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ur_server.bind((ur_server_ip, ur_server_port))
ur_server.listen(1)
print(f"Please connect to the UR3 via TCP ---> {ur_server_ip}:{ur_server_port}")
ur_socket, ur_address = ur_server.accept()
print(f"TCP connection established to UR3 ---> {ur_address}")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("192.168.0.100", 33000))

while True:
    data = ur_server.recv(1024) # Recieve message from UR3
    print(f"Recieved data : {data}")
    client_socket.send(data) # Send that directly to the server
    print(f"Sent data : {data}")
