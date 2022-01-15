import bpy
from .material_env.material_class import Material
from .tools.texture_getter import GetTextureOperator


class PBRPanel(bpy.types.Panel):
    bl_label = "Easy PBR Hook"
    bl_idname = "PBR_PT_Core"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        if 'CURRENT' not in Material.MATERIALS:
            Material(bpy.context.selected_objects[0].active_material.name)
        return context.active_object.active_material is not None

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        Material.MATERIALS['CURRENT'].current_path = material_prop.conf_path
        Material.MATERIALS['CURRENT'].current_pattern = material_prop.texture_pattern
        layout = self.layout
        if PBRPanel.is_bad_state(layout):
            return
        PBRPanel.update_material()
        row = layout.row()
        row.prop(material_prop, "conf_path")
        row = layout.row()
        row.prop(material_prop, "texture_pattern")
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
            row.label(text="No object")
            return True
        if bpy.context.selected_objects[0].active_material is None:
            row = layout.row()
            row.label(text="No material")
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

