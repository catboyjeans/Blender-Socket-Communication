import struct
import socket 

#TCP_IP=socket.gethostname()
TCP_IP="127.0.0.1"
TCP_PORT=2001
BUFFER_SIZE=1024

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind((TCP_IP,TCP_PORT))
serversocket.listen(3)
#s.accept waits for the client and tags it 
clientsocket,address=serversocket.accept()
print("Connection stablished \n")


for i in range(50):
    msg1 = struct.pack('>d', 1.1+i)
    clientsocket.send(msg1)


print("connection ended \n")
clientsocket.close()

#data= clientsocket.recv(1024)
#print(data)
