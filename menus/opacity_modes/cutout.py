import bpy
from ...tools.update_tool import update_opacity_add
from ...material_env.material_class import Material

__all__ = ['CutoutMode']


class CutoutMode(bpy.types.Operator):
    bl_idname = "pbr.cutout"
    bl_label = "Cutout"
    bl_description = "cutout mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CLEAR')
        Material.MATERIALS['CURRENT'].opacity_mode = "Cutout"
        context.object.active_material.use_backface_culling = True
        context.object.active_material.blend_method = "CLIP"
        context.object.active_material.shadow_method = "CLIP"
        return {"FINISHED"}


def register():
    bpy.utils.register_class(CutoutMode)


def unregister():
    bpy.utils.unregister_class(CutoutMode)
