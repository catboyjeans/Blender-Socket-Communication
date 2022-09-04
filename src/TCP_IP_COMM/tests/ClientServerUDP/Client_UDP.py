import socket

bufferSize=1024
HOST = 'localhost'               
PORT = 50007                       # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    s.sendall(b'holaa ')