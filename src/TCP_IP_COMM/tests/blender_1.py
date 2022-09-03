import socket 
import struct
import bpy 


#TCP_IP=socket.gethostname()
TCP_IP='localhost'
TCP_PORT=[2001,2002,2003]
BUFFER_SIZE=8

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind((TCP_IP,TCP_PORT))
serversocket.listen(3)

#s.accept waits for the client and tags it 
clientsocket,address=serversocket.accept()
print('Connection address:', address)
print("--------------------Comm has started--------------------")

#recieve data from simulink 
while 1:

    data = clientsocket.recv(BUFFER_SIZE)

    if not data:
        
        print("--------------------Comm has ended--------------------")
        break 
    
    converteddata = struct.unpack('!d',data)[0]
    print("recieved data: ",converteddata)  
    b= converteddata
    

clientsocket.close()



class socket_vectorization:

    def initialization(self,sIP,sPort):
        
        self.bind((sIP,sPort))
    

#data= clientsocket.recv(1024)
#print(data)
