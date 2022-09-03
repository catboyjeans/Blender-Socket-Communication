import socket 
import struct
import bpy 


#TCP_IP=socket.gethostname()
TCP_IP='localhost'
TCP_PORT=2001
BUFFER_SIZE=1024

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind((TCP_IP,TCP_PORT))
serversocket.listen(3)

#s.accept waits for the client and tags it 
clientsocket,address=serversocket.accept()
print('Connection address:', address)
print("--------------------Comm has started--------------------")


#create a cube
#bpy.ops.mesh.primitive_circle_add()
#so= bpy.context.active_object





#recieve data from simulink 
while 1:

    data = clientsocket.recv(BUFFER_SIZE)
    #converteddata = int.from_bytes(data, byteorder='big', signed=False)

    if not data:
        
        print("--------------------Comm has ended--------------------")
        break 
    
    # converteddata = struct.unpack('!d',data)
    print("recieved data: ",data)  
    # print(type(data))
    # print(type(converteddata))
    # b= converteddata[0]
    # print(len(converteddata))
    # print(b+13)
    


    
        

    

clientsocket.close()


#data= clientsocket.recv(1024)
#print(data)
