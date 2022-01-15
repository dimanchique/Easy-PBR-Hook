import bpy
from ...tools.place_funcs import place_manual

__all__ = ['MetalSmoothnessTexturer']


class MetalSmoothnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metsm"
    bl_label = "Metal Sm."
    bl_description = "Create Metal Smothness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalSmoothness")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(MetalSmoothnessTexturer)


def unregister():
    bpy.utils.unregister_class(MetalSmoothnessTexturer)
