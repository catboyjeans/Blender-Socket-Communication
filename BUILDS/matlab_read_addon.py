bl_info = {
    "name": "New Object",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
import bpy
import h5py
import os
from bpy.props import (StringProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )




class LayoutDemoPanel(bpy.types.Panel):
    
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Matlab Map Keyframe Addon"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        # Keyframe button
        layout.label(text="Map Keyframe data:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.matlab_keyframe_data")

        #Delete Keyframe button
        layout.label(text="Delete Keyframe data:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.matlab_delete_keyframe_data") 

        # #Browse for File 
        # layout.label(text="Select .mat File")
        # scn = context.scene
        # col = layout.column(align=True)
        # col.prop(scn.my_tool, "path", text="")




def button_delete_keyframes(context):
    obj=bpy.context.active_object
    obj.animation_data_clear()
    obj.delta_location=(0,0,0)
    obj.delta_rotation_euler=(0,0,0)


def button_keyframe(context):

    #obj can be anything, change here for selected instead of a named one
    framerate=bpy.context.scene.render.fps

    # obj=current_scene.objects['Cube']
    obj=bpy.context.active_object

    #get data from mat file----------------------------------------------
    filename='test_2.mat'
    directory=r'C:\Users\david\Desktop'
    fullpath=os.path.join(directory,filename)

    f = h5py.File(fullpath)
    data_array=f['ans']

    data_time=data_array[:,0]
    data_x=data_array[:,1]
    data_y=data_array[:,2]
    data_z=data_array[:,3]
    data_rot_x=data_array[:,4]
    data_rot_y=data_array[:,5]
    data_rot_z=data_array[:,6]

    #map keyframes--------------------------------------------------------

    for i in range(len(data_time)):
        
        # obj.delta_location=(data_x[i],data_y[i],data_z[i])
        obj.delta_location=(0,0,0)
        obj.delta_rotation_euler=(data_rot_x[i],data_rot_y[i],data_rot_z[i]) 
    
        obj.keyframe_insert(data_path="delta_location",frame=data_time[i]*framerate)
        obj.keyframe_insert(data_path="delta_rotation_euler",frame=data_time[i]*framerate)

# class MyProperties(PropertyGroup):

#     path : StringProperty(
#         name="",
#         description="Path to Directory",
#         default="",
#         maxlen=1024,
#         subtype='DIR_PATH')
        

class delete_keyframes_operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.matlab_delete_keyframe_data"
    bl_label = "Deletes keyframes data from mat file"

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        button_delete_keyframes(context)
        return {'FINISHED'}


class mat_read_operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.matlab_keyframe_data"
    bl_label = "Keyframes data from mat file"

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def execute(self, context):
        button_keyframe(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(mat_read_operator)
    bpy.utils.register_class(delete_keyframes_operator)
    bpy.utils.register_class(LayoutDemoPanel)
    # bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)    

def unregister():
    bpy.utils.unregister_class(mat_read_operator)
    bpy.utils.unregister_class(delete_keyframes_operator)
    bpy.utils.unregister_class(LayoutDemoPanel)
    # del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()

    # test call
    # bpy.ops.object.matlab_keyframe_data()
