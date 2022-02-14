import bpy
from ..material_class import Material
from ..tools.place_nodes import place_manual

__all__ = ['PipelineMenu']


class PipelineMenu(bpy.types.Operator):
    bl_idname = "pbr.pipeline_menu"
    bl_label = "Change Pipeline"
    bl_description = "Set material pipeline"

    @staticmethod
    def execute(self, context):
        context.window_manager.popup_menu(PipelineMenu.show_menu, title="Found pipelines")
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        textures = Material.MATERIALS['CURRENT']
        if Material.pipelines_found():
            if textures.found_textures["ORM"]:
                layout.operator(ORMPipeline.bl_idname, text="ORM")
                if textures.found_textures["Color Mask"]:
                    layout.operator(ORMMSKPipeline.bl_idname, text="ORM+MSK")
            if textures.found_textures["Metal Smoothness"]:
                layout.operator(MetalSmoothnessPipeline.bl_idname, text="Metal Smoothness")
            if textures.found_textures["Metal"] or textures.found_textures["Roughness"]:
                if textures.found_textures["Metal"] and textures.found_textures["Roughness"]:
                    text = "Metal+Roughness"
                elif textures.found_textures["Metal"]:
                    text = "Metal"
                else:
                    text = "Roughness"
                layout.operator(MetalRoughnessPipeline.bl_idname, text=text)
        else:
            layout.label(text="No options")


class ORMPipeline(bpy.types.Operator):
    bl_idname = "pbr.orm"
    bl_label = "ORM"
    bl_description = "Create ORM Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM")
        return {"FINISHED"}


class ORMMSKPipeline(bpy.types.Operator):
    bl_idname = "pbr.orm_msk"
    bl_label = "ORM+MSK"
    bl_description = "Create ORM+MSK Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM+MSK")
        return {"FINISHED"}


class MetalRoughnessPipeline(bpy.types.Operator):
    bl_idname = "pbr.metal_roughness"
    bl_label = "MetalRoughness"
    bl_description = "Create Metal/Roughness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalRoughness")
        return {"FINISHED"}


class MetalSmoothnessPipeline(bpy.types.Operator):
    bl_idname = "pbr.met_sm"
    bl_label = "Metal Sm."
    bl_description = "Create Metal Smoothness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalSmoothness")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(PipelineMenu)
    bpy.utils.register_class(ORMPipeline)
    bpy.utils.register_class(ORMMSKPipeline)
    bpy.utils.register_class(MetalRoughnessPipeline)
    bpy.utils.register_class(MetalSmoothnessPipeline)


def unregister():
    bpy.utils.unregister_class(PipelineMenu)
    bpy.utils.unregister_class(ORMPipeline)
    bpy.utils.unregister_class(ORMMSKPipeline)
    bpy.utils.unregister_class(MetalRoughnessPipeline)
    bpy.utils.unregister_class(MetalSmoothnessPipeline)
