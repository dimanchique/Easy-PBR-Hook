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

        row = layout.row()
        row.enabled = textures.found_textures["ORM"]
        row.operator(ORMPipeline.bl_idname, text="ORM")

        row = layout.row()
        row.enabled = textures.found_textures["Color Mask"]
        row.operator(ORMMSKPipeline.bl_idname, text="ORM+MSK")

        row = layout.row()
        row.enabled = textures.found_textures["Metal Smoothness"]
        row.operator(MetalSmoothnessPipeline.bl_idname, text="Metal Smoothness")

        text = "Metal+Roughness"
        if textures.found_textures["Metal"] or textures.found_textures["Roughness"]:
            if textures.found_textures["Metal"] and textures.found_textures["Roughness"]:
                text = "Metal+Roughness"
            elif textures.found_textures["Metal"]:
                text = "Metal"
            else:
                text = "Roughness"

        row = layout.row()
        row.enabled = textures.found_textures["Metal"] or textures.found_textures["Roughness"]
        row.operator(MetalRoughnessPipeline.bl_idname, text=text)


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
