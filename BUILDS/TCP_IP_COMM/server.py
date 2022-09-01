import socket


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),2001))
s.listen(5)


while True:
    clientsocket,address=s.accept()
    print("Connection from has been establisjed")
    clientsocket.send(bytes("helooooooooooooo","utf-8"))