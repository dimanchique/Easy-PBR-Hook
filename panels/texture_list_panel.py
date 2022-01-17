import bpy
from ..material_class import Material

__all__ = ['TextureListPanel']


class TextureListPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_Textures_List"
    bl_space_type = "PROPERTIES"
    bl_label = "Found Textures"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return Material.MATERIALS['CURRENT'].finished

    def draw(self, context):
        layout = self.layout
        for texture in Material.MATERIALS['CURRENT'].found:
            if Material.MATERIALS['CURRENT'].found[texture]:
                row = layout.row()
                row.label(text=f"{texture}:")
                sub = row.row()
                sub.label(text=f"{Material.MATERIALS['CURRENT'].images[texture].name}")


def register():
    bpy.utils.register_class(TextureListPanel)


def unregister():
    bpy.utils.unregister_class(TextureListPanel)
