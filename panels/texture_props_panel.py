import bpy
from ..material_class import Material
from ..menus.detail_mask_menu import DetailMaskMenu

__all__ = ['TexturePropsPanel']


class TexturePropsPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_Textures_Props"
    bl_space_type = "PROPERTIES"
    bl_label = "Texture Properties"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return Material.MATERIALS['CURRENT'].finished

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        layout = self.layout
        if not Material.MATERIALS['CURRENT'].found["Albedo"]:
            row = layout.row()
            row.prop(material_prop, "AlbedoColor")
        if "Normal Map" in Material.MATERIALS['CURRENT'].nodes_list:
            row = layout.row()
            row.prop(material_prop, "NormaMapStrength")
            row = layout.row()
            row.prop(material_prop, "NormalMapInverterEnabled")
            if "NormalMix" in context.object.active_material.node_tree.nodes:
                row = layout.row()
                row.prop(material_prop, "DetailMapInverterEnabled")
                if "Detail Mask" not in Material.MATERIALS['CURRENT'].nodes_list and \
                        Material.MATERIALS['CURRENT'].mask_source == "None":
                    row = layout.row()
                    row.prop(material_prop, "DetailMaskStrength")
                row = layout.row()
                row.operator(DetailMaskMenu.bl_idname)
                row = layout.row()
        TexturePropsPanel.show_prop(context, layout,
                                    ["Metal", "ORM", "Metal Smoothness"],
                                    ["MetallicAdd"])
        TexturePropsPanel.show_prop(context, layout,
                                    ["Roughness", "ORM", "Metal Smoothness"],
                                    ["RoughnessAdd"])
        TexturePropsPanel.show_prop(context, layout,
                                    ["Emission"],
                                    ["EmissionMult"])
        TexturePropsPanel.show_prop(context, layout,
                                    ["ORM", "Occlusion"],
                                    ["AO_Strength"])
        TexturePropsPanel.show_prop(context, layout,
                                    ["Specular"],
                                    ["SpecularAdd"])
        TexturePropsPanel.show_prop(context, layout,
                                    ["Color Mask"],
                                    ["MixR", "MixG", "MixB"],
                                    header="Color mask settings:")

    @staticmethod
    def show_prop(context, layout, textures, properties, header=""):
        material_prop = context.active_object.active_material.props
        if any(texture in Material.MATERIALS['CURRENT'].nodes_list for texture in textures):
            if header != "":
                row = layout.row()
                row.label(text=header)
            for prop in properties:
                row = layout.row()
                row.prop(material_prop, prop)


def register():
    bpy.utils.register_class(TexturePropsPanel)


def unregister():
    bpy.utils.unregister_class(TexturePropsPanel)
