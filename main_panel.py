import bpy
from .material_class import Material
from .tools.texture_loader import GetTextureOperator
from .tools.image_updater import UpdateImagesOperator
from .menus.db_update_menu import DBUpdateMenu
from .properties.material_properties import SharedPath


class PBRPanel(bpy.types.Panel):
    bl_label = "Easy PBR Hook"
    bl_idname = "PBR_PT_Core"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        if not context.selected_objects:
            return False
        elif not context.active_object.active_material:
            return False
        return True

    def draw(self, context):
        layout = self.layout
        material_prop = context.active_object.active_material.props
        PBRPanel.update_material(context)
        row = layout.row()
        row.prop(material_prop, "textures_path")
        row.scale_x = 0.3
        row.operator(SharedPath.bl_idname, text="Set Shared Path")
        row = layout.row()
        row.prop(material_prop, "textures_pattern")
        row = layout.row()
        row.prop(material_prop, "UseMaterialNameAsKeyword")
        sub = row.row()
        sub.operator(DBUpdateMenu.bl_idname, text='Texture naming conventions')
        if context.active_object.active_material.props.textures_path != "":
            PBRPanel.assign_textures(layout, material_prop)

    @classmethod
    def update_material(cls, context):
        material = context.active_object.active_material
        Material.check_material(material.name)
        Material.MATERIALS['CURRENT'].current_path = material.props.textures_path
        Material.MATERIALS['CURRENT'].current_pattern = material.props.textures_pattern

    @classmethod
    def assign_textures(cls, layout, material_prop):
        row = layout.row()
        if Material.MATERIALS['CURRENT'].finished:
            row.operator(GetTextureOperator.bl_idname, text="Reload Material")
            row.scale_x = 0.2
            row.prop(material_prop, "Simplify")
            row = layout.row()
            row.operator(UpdateImagesOperator.bl_idname)
        else:
            row.operator(GetTextureOperator.bl_idname)
            row.scale_x = 0.2
            row.prop(material_prop, "Simplify")


def register():
    bpy.utils.register_class(PBRPanel)


def unregister():
    bpy.utils.unregister_class(PBRPanel)

