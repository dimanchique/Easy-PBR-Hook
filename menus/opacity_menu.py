import bpy
from .opacity_modes.opaque import OpaqueMode
from .opacity_modes.cutout import CutoutMode
from .opacity_modes.fade import FadeMode

__all__ = ['OpacityMenu']


class OpacityMenu(bpy.types.Operator):
    bl_idname = "pbr.showopacitymenu"
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


def register():
    bpy.utils.register_class(OpacityMenu)


def unregister():
    bpy.utils.unregister_class(OpacityMenu)
