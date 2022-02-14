import bpy
from ..material_class import Material

__all__ = ['UVMapPanel']


class UVMapPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Textures_Coordinates"
    bl_idname = "PBR_PT_UV"
    bl_space_type = "PROPERTIES"
    bl_label = "UV"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return Material.MATERIALS['CURRENT'].finished and \
            bpy.data.meshes[context.active_object.data.name].uv_layers

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "UVMap", text="UV Maps")


def register():
    bpy.utils.register_class(UVMapPanel)


def unregister():
    bpy.utils.unregister_class(UVMapPanel)
