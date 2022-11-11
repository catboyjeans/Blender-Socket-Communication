import bpy

class SocketPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_SocketPanel"
    bl_label = "Socket Communication"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Socket"  ####    <------ Creates a custom tab

    def draw(self, context):
        # You can set the property values that should be used when the user
        # presses the button in the UI.
        scene = context.scene
        obj=context.object
        layout=self.layout

        #### layout.operator_context='INVOKE_DEFAULT'
        layout.label(text='Socket Operator')
        col=layout.column()
        col.alignment='CENTER'
        
        ####    This is kind of an external property, instead of adding an implicit property
        ####    to the operator. If done the later way, you wont be able to change the property 
        ####    dynamically/at the panel, at least I didnt find a way, yet...

        col=layout.column(align=False)

        ####    OPERATOR    (Make sure to add the 'INVOKE_DEFAULT' thing)   #### Operators uses the properties from below 
        col.operator('object.modal_socket',text='Create Socket',icon='TRACKING')
        col.scale_y=3
        ####    PROPERTY
        col=layout.box().column(align=False)
        col.prop(obj.socket_settings,'IP_address',text='IP Address')
        col.prop(obj.socket_settings,'port',text= 'Port')
        col.prop(obj.socket_settings,'lock_translation',text='Lock Translation')
        col.prop(obj.socket_settings,'ANIM_STATUS',text='Animate Object')

        col=layout.column(align=True)
        col.scale_y=2
        col.operator('object.matlab_delete_keyframe_data',text='Delete Keyframes',icon='SHAPEKEY_DATA')

        #### Testing hehhe
        # col=layout.column()
        # col.prop(obj,'location')


def register():
    bpy.utils.register_class(SocketPanel)

def unregister():
    bpy.utils.unregister_class(SocketPanel)

if __name__ == "__main__":
    register()