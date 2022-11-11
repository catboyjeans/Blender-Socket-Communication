import bpy 
import threading
from math import pi
from .socketModule import SocketComm


class MODAL_SocketOperator(bpy.types.Operator):
    """Runs a self-contained socket"""
    ####    Implement timer for simulating an event, match this timing event with the framerate, Possible workaround

    bl_idname = "object.modal_socket"
    bl_label = "Modal Timer Operator"

    ####---------------------------------------------Custom Properties
    @classmethod
    def poll(cls,context):
        return context.object.socket_settings.STATUS is not True

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
            self.report({'INFO'},'Socket Killed')
            self.s1.STATUS = False
            self.s1.killer()
            self.o.socket_settings.STATUS=False #### Not binded to anything anymore
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
        
        ####    Checker to see if the object has an already initialized socket
        ####    (Dummy dumb Checker for ppl pressing the button twice :P)
        ####    Bind Socket ////////////////////////////
        self.s1=SocketComm(address=self.address)
        print('Socket created Successfully :)')
        self.report({'INFO'},'Socket Started')
        self.o.socket_settings.STATUS=True
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
                
                print('Waiting to recieve')            
                self.s1.recieve()
                
                #### Animate object     ///////////////////////////////////////////////////////////////
    
                if self.o.socket_settings.lock_translation:
                    self.o.delta_location=(0,0,0)
                    self.o.delta_rotation_euler=(self.s1.data[3]*(180/pi),self.s1.data[4]*(180/pi),self.s1.data[5]*(180/pi))
                    print('RECIEVED DATA, TRANSLATION IS LOCKED')
                
                else:
                    self.o.delta_location=(self.s1.data[0],self.s1.data[1],self.s1.data[2])
                    self.o.delta_rotation_euler=(self.s1.data[3]*(180/pi),self.s1.data[4]*(180/pi),self.s1.data[5]*(180/pi))
                    print('RECIEVED DATA, TRANSLATION IS UNLOCKED')
                
                if self.o.socket_settings.ANIM_STATUS:
                    print('in  keys')
                    self.o.keyframe_insert(data_path="delta_location")
                    self.o.keyframe_insert(data_path="delta_rotation_euler")

            except:
                
                print('PROBABLY socket was killed during recieving the last sample')
        
        print('Recieving Loop break raised')

class delete_keyframes_operator(bpy.types.Operator):
    """Deletes animation data"""
    bl_idname = "object.matlab_delete_keyframe_data"
    bl_label = "Deletes keyframes data from mat file"

    def execute(self, context):
        obj=bpy.context.active_object
        obj.animation_data_clear()
        obj.delta_location=(0,0,0)
        obj.delta_rotation_euler=(0,0,0)
        return {'FINISHED'}

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

def register():
    bpy.utils.register_class(MODAL_SocketOperator)
    bpy.utils.register_class(DummyClass)            ##### Testing Class
    bpy.utils.register_class(delete_keyframes_operator)

def unregister():
    bpy.utils.unregister_class(MODAL_SocketOperator)
    bpy.utils.unregister_class(DummyClass)          ##### Testing Class
    bpy.utils.unregister_class(delete_keyframes_operator)

if __name__ == "__main__":
    register()