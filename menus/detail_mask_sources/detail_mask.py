import bpy
from ...tools.create_nodes import *
from ...material_env.material_class import Material

__all__ = ['DetailMaskSource']


class DetailMaskSource(bpy.types.Operator):
    bl_idname = "pbr.detailmasksource"
    bl_label = "DetailMaskSource"
    bl_description = "Link Detail Mask to Normal Mix"

    @staticmethod
    def execute(self, context):
        link_nodes(FROM("Detail Mask", "Color"), TO("NormalMix", "Detail Mask"))
        Material.MATERIALS['CURRENT'].mask_source = "Detail Mask"
        return {"FINISHED"}


def register():
    bpy.utils.register_class(DetailMaskSource)


def unregister():
    bpy.utils.unregister_class(DetailMaskSource)
