import bpy
from ..material_class import Material
from ..tools.place_funcs import place_manual

__all__ = ['PipelineMenu']


class PipelineMenu(bpy.types.Operator):
    bl_idname = "pbr.pipeline_menu"
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


class ORMTexturer(bpy.types.Operator):
    bl_idname = "pbr.orm"
    bl_label = "ORM"
    bl_description = "Create ORM Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM")
        return {"FINISHED"}


class ORMMSKTexturer(bpy.types.Operator):
    bl_idname = "pbr.orm_msk"
    bl_label = "ORM+MSK"
    bl_description = "Create ORM+MSK Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM+MSK")
        return {"FINISHED"}


class MetalRoughnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metal_roughness"
    bl_label = "MetalRoughness"
    bl_description = "Create Metal/Roughness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalRoughness")
        return {"FINISHED"}


class MetalSmoothnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.met_sm"
    bl_label = "Metal Sm."
    bl_description = "Create Metal Smoothness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalSmoothness")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(PipelineMenu)
    bpy.utils.register_class(ORMTexturer)
    bpy.utils.register_class(ORMMSKTexturer)
    bpy.utils.register_class(MetalRoughnessTexturer)
    bpy.utils.register_class(MetalSmoothnessTexturer)


def unregister():
    bpy.utils.unregister_class(PipelineMenu)
    bpy.utils.unregister_class(ORMTexturer)
    bpy.utils.unregister_class(ORMMSKTexturer)
    bpy.utils.unregister_class(MetalRoughnessTexturer)
    bpy.utils.unregister_class(MetalSmoothnessTexturer)
