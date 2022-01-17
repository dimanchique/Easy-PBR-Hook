import bpy
from ..tools.update_tool import update_opacity_add
from ..material_class import Material

__all__ = ['OpacityMenu', 'FadeMode', 'OpaqueMode', 'CutoutMode']


class OpacityMenu(bpy.types.Operator):
    bl_idname = "pbr.show_opacity_menu"
    bl_label = "Opaque"
    bl_description = "Set opacity mode"

    @staticmethod
    def execute(self, context):
        wm = context.window_manager
        wm.popup_menu(OpacityMenu.show_menu)
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        layout.operator(OpaqueMode.bl_idname)
        layout.operator(CutoutMode.bl_idname)
        layout.operator(FadeMode.bl_idname)


class FadeMode(bpy.types.Operator):
    bl_idname = "pbr.fade"
    bl_label = "Fade"
    bl_description = "Set fade mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CREATE')
        Material.MATERIALS['CURRENT'].opacity_mode = "Fade"
        context.object.active_material.use_backface_culling = True
        context.object.active_material.blend_method = "BLEND"
        context.object.active_material.shadow_method = "HASHED"
        return {"FINISHED"}


class OpaqueMode(bpy.types.Operator):
    bl_idname = "pbr.opaque"
    bl_label = "Opaque"
    bl_description = "Set opaque mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CLEAR')
        Material.MATERIALS['CURRENT'].opacity_mode = "Opaque"
        context.object.active_material.use_backface_culling = False
        context.object.active_material.blend_method = "OPAQUE"
        context.object.active_material.shadow_method = "OPAQUE"
        return {"FINISHED"}


class CutoutMode(bpy.types.Operator):
    bl_idname = "pbr.cutout"
    bl_label = "Cutout"
    bl_description = "Set cutout mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CLEAR')
        Material.MATERIALS['CURRENT'].opacity_mode = "Cutout"
        context.object.active_material.use_backface_culling = True
        context.object.active_material.blend_method = "CLIP"
        context.object.active_material.shadow_method = "CLIP"
        return {"FINISHED"}


def register():
    bpy.utils.register_class(OpacityMenu)
    bpy.utils.register_class(FadeMode)
    bpy.utils.register_class(OpaqueMode)
    bpy.utils.register_class(CutoutMode)


def unregister():
    bpy.utils.unregister_class(OpacityMenu)
    bpy.utils.unregister_class(FadeMode)
    bpy.utils.unregister_class(OpaqueMode)
    bpy.utils.unregister_class(CutoutMode)
