import bpy
from ...tools.place_funcs import place_manual

__all__ = ['ORMMSKTexturer']


class ORMMSKTexturer(bpy.types.Operator):
    bl_idname = "pbr.ormmsk"
    bl_label = "ORM+MSK"
    bl_description = "Create ORM+MSK Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM+MSK")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(ORMMSKTexturer)


def unregister():
    bpy.utils.unregister_class(ORMMSKTexturer)
