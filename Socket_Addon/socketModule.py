import socket 
from struct import unpack 

####    STANDALONE MODULE DO NOT EDIT nor ADD BLENDER API IMPLEMENTATIONS

class SocketComm():
        ##  buffersize is 1024 bytes default 

    def __init__(self, address, buffersize=1024, vectorSize=8, dataType='double',samples=1000):      ### Check how **kwargs and *args could be implemented here 
        ##  Setting up the Socket Data Structure Field: Family, Type, Protocol, Local Address, Remote Address
        ##  Actions {socket, bind, connect, listen*, accept*, send*, recv*, sendto, recvfrom, close} (* indicate TCP functions)
        ##  Address is in the form tuple (Address,Process Port)
        self.bufferSize=buffersize
        self.address=address
        self.vectorSize=vectorSize
        self.datatype='double'
        self.datalist=[]
        self.samples=samples
        self.STATUS= True    ##  Implement status as running flag checker
        ##  Format guesser goes here as a self.attribute

        # ##  Start {socket,bind}
        # self.startSocket()
        # ##  Recieve {recvfrom}
        # self.recieve()
        # ##  Kill Connection When done recieving (break the loop at recieve)
        # self.killer()

    def startSocket(self):
        ### Underlying Communication Protocol
        ### UDP - User Datagrap Protocol
        try:
            print("----------------------------- \n    starting connection    \n-----------------------------")
            self.s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind(self.address)
            print('ADDRESS----->>>: ',self.address)
            
        except:
            print("Could not Initialize Socket, try other address X_x") 
   
    def recieve(self):
        """Recieves a sample (Block) of data"""
        ##  Main Listening Loop
        print("----------------------------- \n    recieving data    \n-----------------------------")
        
        self.data, self.clientAddress =self.s.recvfrom(self.bufferSize)
        print("Client Data: ",self.data, " | Client Address: ", self.clientAddress,' | Data type: ',type(self.data))
        print('//////////////////////////////////////')
        
        self.data=self.dataHandler()
        print('Vector: ',self.data)
        print('//////////////////////////////////////')


    def dataHandler(self):

        ##  Format guesser implementation goes here ------------------------
        format='6d'

        if not self.data:
            print('No data Found // Empty data given')
            return None 
        
        try: 
            unpackedData=unpack(format,self.data)
            ##  Record Data
            if len(self.datalist)<self.samples:
                self.datalist.append(unpackedData)
                
            return unpackedData

        except:
            print('data wont match format')
            return None

    def killer(self):

        ## Kill the connection in a "Timely Fashion"
        print("-------Shutting down Connection-------")
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        print("-------Connection Killed x_X-------")
