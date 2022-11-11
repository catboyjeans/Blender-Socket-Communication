import bpy 
import socket
from struct import unpack 
import threading

####    Implementation Class DO NOT EDIT, meant to be used independently from blender :^)

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

####            Input implementations can be included as properties at the invoke stage

class MODAL_SocketOperator(bpy.types.Operator):
    """Runs a self-contained socket"""
    ####    Implement timer for simulating an event, match this timing event with the framerate, Possible workaround

    bl_idname = "object.modal_socket"
    bl_label = "Modal Timer Operator"

    ####---------------------------------------------Custom Properties
    ####---------------------------------------------
    
    def __init__(self):
        print('__init__')
        pass

    def __del__(self):
        print('__del__')
        pass

    def modal(self,context,event):
        #print(event.type)                  ####    <------ Uncomment to see ecent type in window
        
        ##start threading
        if event.type in {'ESC'}:
            print('Process ended', ' Decided to cancel ... ')
            self.s1.STATUS = False
            self.s1.killer()
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self,context,event):
        
        #### Assign object to animate    
        
        self.o = context.active_object
        print('ACTIVE OBJECT:',self.o)

        #### Property implementation goes here ...
        self.PORT = self.o.socket_settings.port                               
        self.HOST = self.o.socket_settings.IP_address

        self.address=(self.HOST,self.PORT)
        self.s1=SocketComm(address=self.address)
        print('Socket created Successfully :)')
        self.s1.startSocket()
        print('Socket Started')

        self.t1=threading.Thread(target=self.recieveSample)
        self.t1.daemon=True
        print('threading starting')
        self.t1.start()
        
        ####    Add modal handler 
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
 
    def recieveSample(self):
        
        while self.s1.STATUS:
            ####    Exception handler
            try:
                
                print('waiting to recieve')            
                self.s1.recieve()

                #### Animate object
                self.o.location=(self.s1.data[0],self.s1.data[1],self.s1.data[2])
                print('recieved somthing')
                
            except:
                
                print('PROBABLY socket was killed during recieving the last sample')
        
        print('Recieving Loop break raised')

class SocketPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_SocketPanel"
    bl_label = "Socket Implementation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Socket"  ####    <------ Creates a custom tab

    def draw(self, context):
        # You can set the property values that should be used when the user
        # presses the button in the UI.
        scene = context.scene
        obj=context.object
        layout=self.layout

        #### layout.operator_context='INVOKE_DEFAULT'

        col=layout.column(align=True)

        ####    This is kind of an external property, instead of adding an implicit property
        ####    to the operator. If done the later way, you wont be able to change the property 
        ####    dynamically/at the panel, at least I didnt find a way, yet...

        ####    OPERATOR    (Make sure to add the 'INVOKE_DEFAULT' thing)
        col.operator('object.dummy_class') #### Operators uses the properties from below
        col.operator('object.modal_socket')
        
        ####    PROPERTY
        col.prop(obj.socket_settings,'port')
        col.prop(obj,'location')    

class DummyClass(bpy.types.Operator):
    """Class made just for prototyping"""
    bl_idname = "object.dummy_class"
    bl_label = "Property Example"
    bl_options = {'REGISTER', 'UNDO'}

    my_float: bpy.props.FloatProperty(name="Some Floating Point")
    my_bool: bpy.props.BoolProperty(name="Toggle Option")
    my_string: bpy.props.StringProperty(name="String Value")

    def execute(self, context):
        obj=context.object
        self.report(
            {'INFO'}, 'F: %.2f  B: %s  S: %r' %
            (self.my_float, self.my_bool, self.my_string)
        )
        print('My float:', self.my_float)
        print('My bool:', self.my_bool)
        print('My string:', self.my_string)
        obj.location[0]=obj.socket_settings.port*.001
        
        return {'FINISHED'}

    def invoke(self,context,event):
        print('INVOKE HEEEEE')
        return self.execute(context)

class SocketSettings(bpy.types.PropertyGroup):
    IP_address:bpy.props.StringProperty(default='localhost')    #### DEFAULT ADDRESS SET TO LOCAL MACHINE
    port:bpy.props.IntProperty(default=50010)                   #### DEFAULT PORT SET TO 5002
    STATUS:bpy.props.BoolProperty(default=True)                 #### DEFAULT LISTENING STATUS SET TO 'AVAILABLE' more on this at the docs
    lock_rotation:bpy.props.BoolProperty(default=True)          #### DEFAULT FLAG TO SET THE LOCATION VECTOR TO (0,0,0)

classes = (
    MODAL_SocketOperator,
    SocketSettings,
    SocketPanel,
    DummyClass,
)

##------------------------------------------Register Classes Handler------------------------------------------##

####    In theory, __init__.py should just include the register handler

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    ####    Register custom property to Object.socket_settings
    bpy.types.Object.socket_settings = bpy.props.PointerProperty(type=SocketSettings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        

if __name__ == "__main__":
    register()
####    bpy.ops.object.modal_socket('INVOKE_DEFAULT')
