import bpy
from ..material_class import Material
from ..menus.pipeline_menu import PipelineMenu

__all__ = ['TextureModePanel']


class TextureModePanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_Textures_Mode"
    bl_space_type = "PROPERTIES"
    bl_label = "Found Textures"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return Material.MATERIALS['CURRENT'].finished

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=Material.get_material_mode())
        row = layout.row()
        row.operator(PipelineMenu.bl_idname)


def register():
    bpy.utils.register_class(TextureModePanel)


def unregister():
    bpy.utils.unregister_class(TextureModePanel)
