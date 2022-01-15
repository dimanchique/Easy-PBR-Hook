import bpy
from ..material_env.material_class import Material
from .detail_mask_sources.albedo_alpha import AlbedoAlphaSource
from .detail_mask_sources.detail_mask import DetailMaskSource
from .detail_mask_sources.none import NoneSource

__all__ = ['DetailMaskMenu']


class DetailMaskMenu(bpy.types.Operator):
    bl_idname = "pbr.detailmaskmenu"
    bl_label = "Change Detail Map Source"
    bl_description = "Set sorce to put in Normal Mix node"

    @staticmethod
    def execute(self, context):
        wm = context.window_manager
        wm.popup_menu(DetailMaskMenu.show_menu, title="Available Detail Mask Sources:")
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        if Material.MATERIALS['CURRENT'].found["Detail Mask"]:
            layout.operator(DetailMaskSource.bl_idname, text="Detail Mask")
        if Material.MATERIALS['CURRENT'].found["Albedo"]:
            layout.operator(AlbedoAlphaSource.bl_idname, text="Albedo Alpha")
        layout.operator(NoneSource.bl_idname, text="None")


def register():
    bpy.utils.register_class(DetailMaskMenu)


def unregister():
    bpy.utils.unregister_class(DetailMaskMenu)
