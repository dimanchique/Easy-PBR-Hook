import bpy
from ..material_env.material_class import Material

__all__ = ['TextureCoordinatesPanel']


class TextureCoordinatesPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_TexturesCoordinates"
    bl_space_type = "PROPERTIES"
    bl_label = "Texture Coordinates"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        if not bpy.context.selected_objects:
            return False
        return Material.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material is not None and \
               "Mapping" in context.object.active_material.node_tree.nodes

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        layout = self.layout
        for prop in ["Location", "Rotation", "Scale"]:
            row = layout.row()
            row.prop(material_prop, prop)


def register():
    bpy.utils.register_class(TextureCoordinatesPanel)


def unregister():
    bpy.utils.unregister_class(TextureCoordinatesPanel)
