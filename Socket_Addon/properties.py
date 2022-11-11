import bpy 

class SocketSettings(bpy.types.PropertyGroup):
    IP_address:bpy.props.StringProperty(default='localhost')    #### DEFAULT ADDRESS SET TO LOCAL MACHINE
    port:bpy.props.IntProperty(default=50010)                   #### DEFAULT PORT SET TO 5002
    STATUS:bpy.props.BoolProperty(default=False)
    ANIM_STATUS:bpy.props.BoolProperty(default=False)                 #### DEFAULT LISTENING STATUS SET TO 'AVAILABLE' more on this at the docs
    lock_translation:bpy.props.BoolProperty(default=True)          #### DEFAULT FLAG TO SET THE LOCATION VECTOR TO (0,0,0)

def register():
    bpy.utils.register_class(SocketSettings)
    bpy.types.Object.socket_settings = bpy.props.PointerProperty(type=SocketSettings)
    

def unregister():
    bpy.utils.unregister_class(SocketSettings)

if __name__ == "__main__":
    register()