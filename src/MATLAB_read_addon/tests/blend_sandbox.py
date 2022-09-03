import bpy
from math import radians 

#create cube
bpy.ops.mesh.primitive_cube_add()
so= bpy.context.active_object

#rotate object
so.rotation_euler[0] += radians(45)

#create modifier
mod_subsurf= so.modifiers.new("Modd",'SUBSURF')

mod_subsurf.levels=3

#bpy.ops.object.shade_smooth()

mesh= so.data

for face in mesh.polygons:
    face.use_smooth=True
    
mod_displace=so.modifiers.new("Displace",'DISPLACE')

new_tex = bpy.data.textures.new("Texture",'DISTORTED_NOISE')
new_tex.noise_scale=2

mod_displace.texture= new_tex

new_mat=bpy.data.materials.new(name="material")
so.data.materials.append(new_mat)

new_mat.use_nodes=True
nodes= new_mat.node_tree.nodes

material_output=nodes.get("Material Output")
node_emission= nodes.new(type='ShaderNodeEmission')

node_emission.inputs[0].default_value=(0.0,0.3,1.0,1) #color
node_emission.inputs[1].default_value= 500.0

links =new_mat.node_tree.links
new_link =links.new(node_emission.outputs[0],material_output.inputs[0])

#new_link=links.new(node_emission.outputs[0],material_output.inputs[0])