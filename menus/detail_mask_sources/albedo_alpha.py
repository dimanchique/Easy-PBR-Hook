import bpy
from ...tools.create_nodes import *
from ...material_env.material_class import Material

__all__ = ['AlbedoAlphaSource']


class AlbedoAlphaSource(bpy.types.Operator):
    bl_idname = "pbr.albedoalphasource"
    bl_label = "AlbedoAlphaSource"
    bl_description = "Link Albedo Alpha to Normal Mix"

    @staticmethod
    def execute(self, context):
        link_nodes(FROM("Albedo", "Alpha"), TO("NormalMix", "Detail Mask"))
        Material.MATERIALS['CURRENT'].mask_source = "Albedo Alpha"
        return {"FINISHED"}


def register():
    bpy.utils.register_class(AlbedoAlphaSource)


def unregister():
    bpy.utils.unregister_class(AlbedoAlphaSource)
