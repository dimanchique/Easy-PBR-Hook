import bpy
from ..material_class import Material, get_mode
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
        if not context.selected_objects:
            return False
        return Material.MATERIALS['CURRENT'].finished and context.active_object.active_material is not None

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if not Material.MATERIALS['CURRENT'].nodes_list:
            row.label(text="Mode: None")
        else:
            row.label(text=get_mode())
        row = layout.row()
        row.operator(PipelineMenu.bl_idname)


def register():
    bpy.utils.register_class(TextureModePanel)


def unregister():
    bpy.utils.unregister_class(TextureModePanel)
