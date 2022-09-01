import socket 
import struct

#TCP_IP=socket.gethostname()
TCP_IP='localhost'
TCP_PORTS=[2001,2002,2003,2004,2005,2006] #[x y z rot_x rot_y rot_z]
BUFFER_SIZE=8

class socket_object:

    def __init__(self,ip,port):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((ip,port))
        self.sock.listen(3)
    
    def accept_connection(self,socket):
        clientsocket,address=socket.accept()
        return clientsocket 
       

socket_x=socket_object(TCP_IP,TCP_PORTS[0])
client_socket_x= socket_x.accept_connection(socket_x.sock)

socket_y=socket_object(TCP_IP,TCP_PORTS[1])
client_socket_y= socket_y.accept_connection(socket_y.sock)

print("CONNECTION IS",client_socket_x,client_socket_y)
print("--------------------Comm has started--------------------")


#recieve data from simulink 
while 1:

    data_x = client_socket_x.recv(BUFFER_SIZE)
    data_y = client_socket_y.recv(BUFFER_SIZE)

    if not data_x:
        
        print("--------------------Comm has ended--------------------")
        break 
    
    converteddata_x = struct.unpack('!d',data_x)[0]
    converteddata_y = struct.unpack('!d',data_y)[0]

    print("recieved data: ",converteddata_x,converteddata_y)  
 
    

client_socket_x.close()
client_socket_y.close()

