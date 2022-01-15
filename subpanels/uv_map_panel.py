import bpy
from ..material_env.material_class import Material

__all__ = ['UVMapPanel']


class UVMapPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_UV"
    bl_space_type = "PROPERTIES"
    bl_label = "UV"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        if not bpy.context.selected_objects:
            return False
        return Material.MATERIALS['CURRENT'].finished and \
            context.active_object.active_material is not None and \
            len(bpy.data.meshes[bpy.context.active_object.data.name].uv_layers.keys()) > 1

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "UVMap", text="List of available UV Maps")


def register():
    bpy.utils.register_class(UVMapPanel)


def unregister():
    bpy.utils.unregister_class(UVMapPanel)
