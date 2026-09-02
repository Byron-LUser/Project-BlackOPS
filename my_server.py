import socket
import threading

SERVER = "0.0.0.0"
PORT = 8888
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)