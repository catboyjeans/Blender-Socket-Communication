import socket

bufferSize=1024
HOST = 'localhost'               
PORT = 50007                       # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    #socket now ready for listening...
    s.listen()
    #recvfrom returns a pair (bytes,address), byte's an object, address is the sender's socket address 
    print("socket now ready for listening ")

    while True:
        clientMsg,clientAddress =s.recvfrom(bufferSize)
        print("Client Data: ",clientMsg, " Client Address: ", clientAddress)
        if not clientMsg: break