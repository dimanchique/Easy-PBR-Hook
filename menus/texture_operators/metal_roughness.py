import bpy
from ...tools.place_funcs import place_manual

__all__ = ['MetalRoughnessTexturer']


class MetalRoughnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metalroughness"
    bl_label = "MetalRoughness"
    bl_description = "Create Metal/Roughness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalRoughness")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(MetalRoughnessTexturer)


def unregister():
    bpy.utils.unregister_class(MetalRoughnessTexturer)
