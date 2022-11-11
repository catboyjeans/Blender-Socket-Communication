bl_info = {
    "name": "Socket Addon",
    "version": (1, 0),
    "author": "M4CH1N3G1RL",
    "blender": (3, 2, 0),
    "location": "View3D >> UI >> Socket Tab",
    "description": "Creates a socket communication channel (UDP) to the selected object, recieving incoming messages at the desired address",
    "doc_url":"",
    "tracker_url":"https://github.com/M4CH1N3G1RL/Blender-Socket-Communication",
    "category": "Object",
}

#### For prototyping purposes
import importlib as imp
#import sys
#sys.path.append(r"C:\Users\david\Documents\codes\python\Blender_Socket_Project")

if "bpy" in locals():

    imp.reload(operators)
    imp.reload(panels)
    imp.reload(properties)

else:
    import bpy                  #### <---- Is it really useful??!
    #### Replace package to . reference to Socket_Addon
    from . import operators
    from . import panels
    from . import properties
    
    imp.reload(operators)
    imp.reload(panels)
    imp.reload(properties)

def register():
    operators.register()
    panels.register()
    properties.register()

def unregister():
    operators.unregister()
    panels.unregister()
    properties.unregister()

if __name__ == "__main__":
    register()