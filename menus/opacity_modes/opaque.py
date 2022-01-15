import bpy
from ...tools.update_tool import update_opacity_add
from ...material_env.material_class import Material

__all__ = ['OpaqueMode']


class OpaqueMode(bpy.types.Operator):
    bl_idname = "pbr.opaque"
    bl_label = "Opaque"
    bl_description = "opaque mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CLEAR')
        Material.MATERIALS['CURRENT'].opacity_mode = "Opaque"
        context.object.active_material.use_backface_culling = False
        context.object.active_material.blend_method = "OPAQUE"
        context.object.active_material.shadow_method = "OPAQUE"
        return {"FINISHED"}


def register():
    bpy.utils.register_class(OpaqueMode)


def unregister():
    bpy.utils.unregister_class(OpaqueMode)
