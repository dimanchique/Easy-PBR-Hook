import bpy
from .material_class import Material
from .tools.texture_getter import GetTextureOperator
from .menus.db_update_menu import DBUpdateMenu


class PBRPanel(bpy.types.Panel):
    bl_label = "Easy PBR Hook"
    bl_idname = "PBR_PT_Core"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        elif context.active_object.active_material is None:
            return False
        else:
            if 'CURRENT' not in Material.MATERIALS:
                Material(context.selected_objects[0].active_material.name)
            return True

    def draw(self, context):
        layout = self.layout
        if PBRPanel.is_bad_state(layout):
            return
        material_prop = context.active_object.active_material.props
        Material.MATERIALS['CURRENT'].current_path = material_prop.conf_path
        Material.MATERIALS['CURRENT'].current_pattern = material_prop.texture_pattern
        PBRPanel.update_material()
        row = layout.row()
        row.prop(material_prop, "conf_path")
        row = layout.row()
        row.prop(material_prop, "texture_pattern")
        row = layout.row()
        row.prop(material_prop, "UseMaterialNameAsKeyword")
        row = layout.row()
        row.operator(DBUpdateMenu.bl_idname, text='Update textures masks')
        PBRPanel.assign_textures(layout)

    @staticmethod
    def update_material():
        material_name = bpy.context.selected_objects[0].active_material.name
        if 'CURRENT' not in Material.MATERIALS:
            Material(material_name)
        elif Material.MATERIALS['CURRENT'].name != material_name:
            if material_name not in Material.MATERIALS:
                Material(material_name)
            else:
                Material.MATERIALS['CURRENT'] = Material.MATERIALS[material_name]

    @staticmethod
    def is_bad_state(layout):
        if not bpy.context.selected_objects:
            row = layout.row()
            row.label(text="No active object")
            return True
        if bpy.context.selected_objects[0].active_material is None:
            row = layout.row()
            row.label(text="No active material")
            if 'CURRENT' in Material.MATERIALS:
                Material.MATERIALS['CURRENT'].finished = False
            return True
        return False

    @staticmethod
    def assign_textures(layout):
        row = layout.row()
        text = "Reassign textures" if Material.MATERIALS['CURRENT'].finished else "Assign textures"
        row.operator(GetTextureOperator.bl_idname, text=text)


def register():
    bpy.utils.register_class(PBRPanel)


def unregister():
    bpy.utils.unregister_class(PBRPanel)

