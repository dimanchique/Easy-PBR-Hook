import bpy
from ...tools.update_tool import update_opacity_add
from ...material_env.material_class import Material

__all__ = ['FadeMode']


class FadeMode(bpy.types.Operator):
    bl_idname = "pbr.fade"
    bl_label = "Fade"
    bl_description = "fade mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CREATE')
        Material.MATERIALS['CURRENT'].opacity_mode = "Fade"
        context.object.active_material.use_backface_culling = True
        context.object.active_material.blend_method = "BLEND"
        context.object.active_material.shadow_method = "HASHED"
        return {"FINISHED"}


def register():
    bpy.utils.register_class(FadeMode)


def unregister():
    bpy.utils.unregister_class(FadeMode)
