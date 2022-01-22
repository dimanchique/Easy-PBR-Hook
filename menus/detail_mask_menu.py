import bpy
from ..material_class import Material
from ..tools.create_nodes import *
from ..tools.place_nodes import *
from ..tools.misc import DETAIL_MASK_PLACED, DETAIL_MASK_REMOVED

__all__ = ['DetailMaskMenu']


class DetailMaskMenu(bpy.types.Operator):
    bl_idname = "pbr.detail_mask_menu"
    bl_label = "Change Detail Mask Source"
    bl_description = "Set source to put in Normal Mix node"

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


class AlbedoAlphaSource(bpy.types.Operator):
    bl_idname = "pbr.albedo_alpha_source"
    bl_label = "AlbedoAlphaSource"
    bl_description = "Link Albedo Alpha to Normal Mix"

    @staticmethod
    def execute(self, context):
        nodes = bpy.context.object.active_material.node_tree.nodes
        link_nodes(FROM("Albedo", "Alpha"), TO("NormalMix", "Detail Mask"))
        Material.MATERIALS['CURRENT'].mask_source = "Albedo Alpha"
        if "Detail Mask" in nodes:
            remove_detail_mask()
            self.report({'INFO'}, DETAIL_MASK_REMOVED)
        return {"FINISHED"}


class DetailMaskSource(bpy.types.Operator):
    bl_idname = "pbr.detail_mask_source"
    bl_label = "DetailMaskSource"
    bl_description = "Link Detail Mask to Normal Mix"

    @staticmethod
    def execute(self, context):
        nodes = bpy.context.object.active_material.node_tree.nodes
        if "Detail Mask" not in nodes:
            place_detail_mask(new=True)
            self.report({'INFO'}, DETAIL_MASK_PLACED)
        link_nodes(FROM("Detail Mask", "Color"), TO("NormalMix", "Detail Mask"))
        Material.MATERIALS['CURRENT'].mask_source = "Detail Mask"

        return {"FINISHED"}


class NoneSource(bpy.types.Operator):
    bl_idname = "pbr.none_source"
    bl_label = "NoneSource"
    bl_description = "Remove Detail Mask link from Normal Mix"

    @staticmethod
    def execute(self, context):
        Material.MATERIALS['CURRENT'].mask_source = "None"
        nodes = context.object.active_material.node_tree
        if nodes.nodes['NormalMix'].inputs['Detail Mask'].links:
            nodes.links.remove(nodes.nodes['NormalMix'].inputs['Detail Mask'].links[0])
        if "Detail Mask" in nodes.nodes:
            remove_detail_mask()
            self.report({'INFO'}, DETAIL_MASK_REMOVED)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(DetailMaskMenu)
    bpy.utils.register_class(AlbedoAlphaSource)
    bpy.utils.register_class(DetailMaskSource)
    bpy.utils.register_class(NoneSource)


def unregister():
    bpy.utils.unregister_class(DetailMaskMenu)
    bpy.utils.unregister_class(AlbedoAlphaSource)
    bpy.utils.unregister_class(DetailMaskSource)
    bpy.utils.unregister_class(NoneSource)
