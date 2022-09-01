#latest version test sample for blender
import bpy


current_scene=bpy.context.scene
#obj can be anything, change here for selected instead of a named one
framerate=bpy.context.scene.render.fps

obj=current_scene.objects['Cube']



for i in range(0,10):
    
    obj.keyframe_insert(data_path="location",frame=i)


