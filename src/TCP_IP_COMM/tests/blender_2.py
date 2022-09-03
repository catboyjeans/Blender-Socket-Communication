import bpy
import socket
import struct
from math import radians

#SOCKET SETUP-----------------
TCP_IP='localhost'
TCP_PORT=2001
BUFFER_SIZE=8
serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind((TCP_IP,TCP_PORT))
print("--------------------WAITING FOR SIMULINK--------------------") 
serversocket.listen(3)
clientsocket,address=serversocket.accept()
print('Connection address:', address)
print("--------------------Comm has started--------------------")     

#modal operator----------------------------------
class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"
    _timer = None
    print("Estoy en la clase")



    #Cycling action is defined in modal 'TIMER' type
    def modal(self, context, event):
        
        print("estoy en el modal")
        data = clientsocket.recv(BUFFER_SIZE)
        
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # change theme color, silly!
            color = context.preferences.themes[0].view_3d.space.gradients.high_gradient
            color.s = 1.0
            color.h += 0.01
            

            if not data:
                print("--------------------Comm has ended--------------------")
                clientsocket.close()
                serversocket.close()
                self.cancel(context)
                return {'CANCELLED'}
            
            converteddata = struct.unpack('!d',data)[0]
            print("recieved data: ",converteddata)  
            #b= converteddata[0]

            #blender actions 

            bpy.context.active_object.rotation_euler[0]=converteddata
            bpy.context.active_object.rotation_euler[1]=converteddata
            bpy.context.active_object.rotation_euler[2]=converteddata
            #
            #  
            #
            #
        return {'PASS_THROUGH'}


    ''' def socket_startup(self):
        #This method returns the clientsocket used for reading comms
        clientsocket,address=self.accept()
        print('Connection address:', address)
        print("--------------------Comm has started--------------------")
        return clientsocket'''
      
   
    def execute(self, context):
        print("estoy en execute")
        
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        clientsocket.close()
        serversocket.close()
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