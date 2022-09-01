import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),2001))

while True:
    msg = s.recv(62)
    print(msg.decode("utf-8"))