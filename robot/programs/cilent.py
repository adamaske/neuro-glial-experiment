import socket
import time
HOST = "192.168.12.66"
PORT = 50002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
s.send("freedrive_mode()" + "\n")
data = s.recv(1024)
print(data.decode())

time.sleep(1)
s.send("end_freedrive_mode()" + "\n")