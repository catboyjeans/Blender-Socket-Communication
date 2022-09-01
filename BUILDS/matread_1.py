import bpy
import h5py
import os 

current_scene=bpy.context.scene
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

 