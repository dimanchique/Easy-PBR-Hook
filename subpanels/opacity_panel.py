import bpy
from ..material_env.material_class import Material
from ..menus.opacity_menu import OpacityMenu
from ..tools.misc import TEXTURES

__all__ = ['OpacityPanel']


class OpacityPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_opacity_mode"
    bl_space_type = "PROPERTIES"
    bl_label = "Opacity Settings"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        if 'CURRENT' in Material.MATERIALS:
            return (Material.MATERIALS['CURRENT'].opacity_from_albedo
                    or Material.MATERIALS['CURRENT'].found["Opacity"]) \
                   and Material.MATERIALS['CURRENT'].finished \
                   and context.active_object.active_material is not None\
                   and context.selected_objects != []
        return False

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Opacity Mode:")
        row.operator(OpacityMenu.bl_idname, text=Material.MATERIALS['CURRENT'].opacity_mode)
        material_prop = context.active_object.active_material.props
        if Material.MATERIALS['CURRENT'].opacity_mode == "Cutout":
            row = layout.row()
            row.prop(context.active_object.active_material.props, "AlphaThreshold")
        if Material.MATERIALS['CURRENT'].opacity_mode == "Fade":
            row = layout.row()
            row.prop(material_prop, "AlphaMode")
            row = layout.row()
            row.prop(material_prop, "OpacityAdd")


def register():
    bpy.utils.register_class(OpacityPanel)


def unregister():
    bpy.utils.unregister_class(OpacityPanel)
