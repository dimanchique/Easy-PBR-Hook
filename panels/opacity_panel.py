import bpy
from ..material_class import Material
from ..menus.opacity_menu import OpacityMenu

__all__ = ['OpacityPanel']


class OpacityPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_Opacity_Mode"
    bl_space_type = "PROPERTIES"
    bl_label = "Opacity Settings"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        return Material.MATERIALS['CURRENT'].finished and \
               (Material.MATERIALS['CURRENT'].opacity_from_albedo or
                Material.MATERIALS['CURRENT'].found_textures["Opacity"])

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Opacity Mode:")
        row.operator(OpacityMenu.bl_idname, text=Material.MATERIALS['CURRENT'].opacity_mode)
        material_prop = context.active_object.active_material.props
        if Material.MATERIALS['CURRENT'].opacity_mode == "Cutout":
            row = layout.row()
            row.prop(context.active_object.active_material.props, "AlphaThreshold")
        elif Material.MATERIALS['CURRENT'].opacity_mode == "Fade":
            row = layout.row()
            row.prop(material_prop, "AlphaMode")
            row = layout.row()
            row.prop(material_prop, "OpacityAdd")


def register():
    bpy.utils.register_class(OpacityPanel)


def unregister():
    bpy.utils.unregister_class(OpacityPanel)
