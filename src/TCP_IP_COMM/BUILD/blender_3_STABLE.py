import bpy
import socket
import struct
    

#modal operator----------------------------------
class ModalTimerOperator(bpy.types.Operator):

    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    _timer = None
    # print("Estoy en la class")

    #SOCKET SETUP-----------------
    
    # TCP_IP=socket.gethostname()
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

    print("--------------------WAITING FOR SIMULINK--------------------") 
    #SOCKET CONFIGURARION POSITION--------------------------------------------------------
    socket_x=socket_object(TCP_IP,TCP_PORTS[0])
    client_socket_x= socket_x.accept_connection(socket_x.sock)

    socket_y=socket_object(TCP_IP,TCP_PORTS[1])
    client_socket_y= socket_y.accept_connection(socket_y.sock)

    socket_z=socket_object(TCP_IP,TCP_PORTS[2])
    client_socket_z= socket_z.accept_connection(socket_z.sock)

    #SOCKET CONFIGURARION POSITION--------------------------------------------------------      
    socket_rx=socket_object(TCP_IP,TCP_PORTS[3])
    client_socket_rx= socket_rx.accept_connection(socket_rx.sock)

    socket_ry=socket_object(TCP_IP,TCP_PORTS[4])
    client_socket_ry= socket_ry.accept_connection(socket_ry.sock)

    socket_rz=socket_object(TCP_IP,TCP_PORTS[5])
    client_socket_rz= socket_rz.accept_connection(socket_rz.sock)



    print("CONNECTION IS",client_socket_x,client_socket_y)
    print("--------------------Comm has started--------------------")   


    #Cycling action is defined in modal 'TIMER' type
    def modal(self, context, event):
        
        # print("estoy en el modal")
        #TE QUEDASTE AQUI--------------------------------------
        data_x = self.client_socket_x.recv(self.BUFFER_SIZE)
        data_y = self.client_socket_y.recv(self.BUFFER_SIZE)
        data_z = self.client_socket_z.recv(self.BUFFER_SIZE)
        data_rx = self.client_socket_rx.recv(self.BUFFER_SIZE)
        data_ry = self.client_socket_ry.recv(self.BUFFER_SIZE)
        data_rz = self.client_socket_rz.recv(self.BUFFER_SIZE)
        
        # if event.type in {'RIGHTMOUSE', 'ESC'}:
        #     self.cancel(context)
        #     return {'CANCELLED'}

        if event.type == 'TIMER':
            # change theme color, silly!
            # color = context.preferences.themes[0].view_3d.space.gradients.high_gradient
            # color.s = 1.0
            # color.h += 0.01
    

            if not data_x:
                print("--------------------Comm has ended--------------------")
                #close client and server closets for future blender runs
                self.client_socket_x.close()
                self.socket_x.sock.close()
                self.client_socket_y.close()
                self.socket_y.sock.close()
                self.client_socket_z.close()
                self.socket_z.sock.close()
                self.client_socket_rx.close()
                self.socket_rx.sock.close()
                self.client_socket_ry.close()
                self.socket_ry.sock.close()
                self.client_socket_rz.close()
                self.socket_rz.sock.close()
                self.cancel(context)
                return {'CANCELLED'}
            

            #data decrypt done by struct module ----------------------------------------

            converteddata_x = struct.unpack('!d',data_x)[0]
            converteddata_y = struct.unpack('!d',data_y)[0]
            converteddata_z = struct.unpack('!d',data_z)[0]
            converteddata_rx = struct.unpack('!d',data_rx)[0]
            converteddata_ry = struct.unpack('!d',data_ry)[0]
            converteddata_rz = struct.unpack('!d',data_rz)[0]

            print("recieved data: ",converteddata_x,converteddata_y,converteddata_z,converteddata_rx,converteddata_ry,converteddata_rz)   

            #blender actions 
            bpy.context.active_object.location[0]=converteddata_x
            bpy.context.active_object.location[1]=converteddata_y
            bpy.context.active_object.location[2]=converteddata_z
            bpy.context.active_object.rotation_euler[0]=converteddata_rx
            bpy.context.active_object.rotation_euler[1]=converteddata_ry
            bpy.context.active_object.rotation_euler[2]=converteddata_rz
            #
            #  
            #
            #
        return {'PASS_THROUGH'}


    def execute(self, context):
        # print("estoy en execute")
        
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        # print("estoy en cancel")
        self.client_socket_x.close()
        self.socket_x.sock.close()
        self.client_socket_y.close()
        self.socket_y.sock.close()
        self.client_socket_z.close()
        self.socket_z.sock.close()
        self.client_socket_rx.close()
        self.socket_rx.sock.close()
        self.client_socket_ry.close()
        self.socket_ry.sock.close()
        self.client_socket_rz.close()
        self.socket_rz.sock.close()
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
       


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()