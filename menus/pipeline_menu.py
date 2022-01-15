import bpy
from ..material_env.material_class import Material
from .texture_operators.orm import ORMTexturer
from .texture_operators.orm_msk import ORMMSKTexturer
from .texture_operators.metal_roughness import MetalRoughnessTexturer
from .texture_operators.metal_smoothness import MetalSmoothnessTexturer


__all__ = ['PipelineMenu']


class PipelineMenu(bpy.types.Operator):
    bl_idname = "pbr.pipelinemenu"
    bl_label = "Change Pipeline"
    bl_description = "Set pipeline (ORM/MetalSmoothness/etc.)"

    @staticmethod
    def execute(self, context):
        wm = context.window_manager
        wm.popup_menu(PipelineMenu.show_menu, title="Found pipelines")
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        text = ''
        if Material.MATERIALS['CURRENT'].found["ORM"]:
            layout.operator(ORMTexturer.bl_idname, text="ORM")
            if Material.MATERIALS['CURRENT'].found["Color Mask"]:
                layout.operator(ORMMSKTexturer.bl_idname, text="ORM+MSK")
        if Material.MATERIALS['CURRENT'].found["Metal Smoothness"]:
            layout.operator(MetalSmoothnessTexturer.bl_idname, text="Metal Smoothness")
        if Material.MATERIALS['CURRENT'].found["Metal"] or Material.MATERIALS['CURRENT'].found["Roughness"]:
            if Material.MATERIALS['CURRENT'].found["Metal"] and Material.MATERIALS['CURRENT'].found["Roughness"]:
                text = "Metal+Roughness"
            elif Material.MATERIALS['CURRENT'].found["Metal"]:
                text = "Metal"
            elif Material.MATERIALS['CURRENT'].found["Roughness"]:
                text = "Roughness"
            layout.operator(MetalRoughnessTexturer.bl_idname, text=text)
        if not any(texture in Material.MATERIALS['CURRENT'].found for texture in
                   ["ORM", "Metal Smoothness", "Metal", "Roughness"]):
            layout.label(text="No options")


def register():
    bpy.utils.register_class(PipelineMenu)


def unregister():
    bpy.utils.unregister_class(PipelineMenu)
