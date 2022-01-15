import bpy
from ...tools.place_funcs import place_manual

__all__ = ['ORMTexturer']


class ORMTexturer(bpy.types.Operator):
    bl_idname = "pbr.orm"
    bl_label = "ORM"
    bl_description = "Create ORM Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(ORMTexturer)


def unregister():
    bpy.utils.unregister_class(ORMTexturer)
