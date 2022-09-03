bl_info = {
    "name": "Matlab Keyframe Data Import",
    "author": "Torres",
    "version": (1.2, 0),
    "blender": (2, 80, 0),
    "location": "Object Properties",
    "description": "Maps keyframed data from mat file, mat file should not be a time object",
    "warning": "",
    "doc_url": "",
    "category": "Keyframe Mapping",
}



from contextlib import nullcontext
import bpy
import random 
import h5py
import numpy as np
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
        
        #Browse for File 
        layout.label(text="Selected .mat file:")
        scn = bpy.context.scene
        col = layout.column(align=True)
        col.prop(scn.my_directory, "path", text="")
        #Keyframe button
        layout.label(text="Map Keyframe data:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.matlab_keyframe_data")

        #Delete Keyframe button
        layout.label(text="Delete Keyframe data:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.matlab_delete_keyframe_data") 

        #Trail button
        layout.label(text="Plot the objects trail:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.plot_trail")

      
def  store(time):
    time



def button_delete_keyframes(context):
    obj=bpy.context.active_object
    obj.animation_data_clear()
    obj.delta_location=(0,0,0)
    obj.delta_rotation_euler=(0,0,0)


def button_keyframe(context):

    #obj can be anything, change here for selected instead of a named one
    framerate=bpy.context.scene.render.fps

    obj=bpy.context.active_object
    scn = bpy.context.scene
    #get data from mat file----------------------------------------------
    # filename='test_2.mat'
    # directory=r'C:\Users\david\Desktop'
    # fullpath=os.path.join(directory,filename)
    #f = h5py.File(fullpath)
    
    f=h5py.File(scn.my_directory.path)
    data_array=f['ans']

    
    data_time=data_array[:,0]
    data_x=data_array[:,1]
    data_y=data_array[:,2]
    data_z=data_array[:,3]
    data_rot_x=np.radians(data_array[:,4])
    data_rot_y=np.radians(data_array[:,5])
    data_rot_z=np.radians(data_array[:,6])

    #map keyframes--------------------------------------------------------

    for i in range(len(data_time)):
        
        obj.delta_location=(data_x[i],data_y[i],data_z[i])
        obj.delta_rotation_euler=(data_rot_x[i],data_rot_y[i],data_rot_z[i]) 
    
        obj.keyframe_insert(data_path="delta_location",frame=data_time[i]*framerate)
        obj.keyframe_insert(data_path="delta_rotation_euler",frame=data_time[i]*framerate)

def button_trail(context):
    
    ob = bpy.context.object

    #retrieve animation data
    def get_keyframes_info(object):
    
        range=object.animation_data.action.frame_range
        return range


    if ob.animation_data:
        print("a")
        range = get_keyframes_info(ob)
        print(range)
        
    elif ob.constraints:
        print("b")
        target_object=ob.constraints[0].target
        range = get_keyframes_info(target_object)
        print(range)

    else:
        print("object has no animation data nor constraints")
    


    bpy.ops.object.paths_calculate(start_frame=range[0],end_frame=range[1]) ## might fix solid definitions later
    
    mp = ob.motion_path

    if mp:
        path = bpy.data.curves.new('path','CURVE')
        curve = bpy.data.objects.new('Curve',path)
        bpy.context.scene.collection.objects.link(curve)
        path.dimensions = '3D'
        spline = path.splines.new('BEZIER')
        spline.bezier_points.add(len(mp.points)-1)
        
        for i,o in enumerate(spline.bezier_points):
            o.co = mp.points[i].co
            o.handle_right_type = 'AUTO'
            o.handle_left_type = 'AUTO' 

    path.bevel_depth=.01
    path.resolution_u=2
    path.bevel_factor_end=0
    path.bevel_factor_start=0
    path.keyframe_insert(data_path="bevel_factor_start",frame=range[0])
    path.bevel_factor_start=1
    path.keyframe_insert(data_path="bevel_factor_start",frame=range[1]) 
            
    bpy.ops.object.paths_clear()

    ##create random material
    ##--------------------------------------------------------------------------------------------------------
    material=bpy.data.materials.new(name="random")
    material.use_nodes= True

    material_output_node=material.node_tree.nodes['Material Output']
    emission_node=material.node_tree.nodes.new('ShaderNodeEmission')
    color_node=material.node_tree.nodes.new('ShaderNodeHueSaturation')

    color_node.inputs[0].default_value=random.uniform(0,1)
    color_node.inputs[4].default_value=(1,0,0,1)


    link=material.node_tree.links.new

    link(color_node.outputs[0],emission_node.inputs[0])
    link(emission_node.outputs[0],material_output_node.inputs[0])

    curve.active_material=material



class delete_keyframes_operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.matlab_delete_keyframe_data"
    bl_label = "Deletes keyframes data from mat file"

    def execute(self, context):
        button_delete_keyframes(context)
        return {'FINISHED'}


class mat_read_operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.matlab_keyframe_data"
    bl_label = "Keyframes data from mat file"

    def execute(self, context):
        button_keyframe(context)
        return {'FINISHED'}

class plot_trail(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.plot_trail"
    bl_label = "Plots the object's trail"

    def execute(self, context):
        button_trail(context)
        return {'FINISHED'}

class DirectoryPath(PropertyGroup):

    path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')


def register():
    bpy.utils.register_class(mat_read_operator)
    bpy.utils.register_class(delete_keyframes_operator)
    bpy.utils.register_class(LayoutDemoPanel)
    bpy.utils.register_class(DirectoryPath)
    bpy.utils.register_class(plot_trail)
    bpy.types.Scene.my_directory = PointerProperty(type=DirectoryPath)

  

def unregister():
    bpy.utils.unregister_class(mat_read_operator)
    bpy.utils.unregister_class(delete_keyframes_operator)
    bpy.utils.unregister_class(LayoutDemoPanel)
    bpy.utils.unregister_class(DirectoryPath)
    bpy.utils.unregister_class(plot_trail)
    del bpy.types.Scene.my_directory


if __name__ == "__main__":
    register()
