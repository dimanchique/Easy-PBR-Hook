import bpy
from ...material_env.material_class import Material

__all__ = ['NoneSource']


class NoneSource(bpy.types.Operator):
    bl_idname = "pbr.nonesource"
    bl_label = "NoneSource"
    bl_description = "Remove Detail Mask link from Normal Mix"

    @staticmethod
    def execute(self, context):
        Material.MATERIALS['CURRENT'].mask_source = "None"
        nodes = context.object.active_material.node_tree
        if nodes.nodes['NormalMix'].inputs['Detail Mask'].links != ():
            nodes.links.remove(nodes.nodes['NormalMix'].inputs['Detail Mask'].links[0])
        return {"FINISHED"}


def register():
    bpy.utils.register_class(NoneSource)


def unregister():
    bpy.utils.unregister_class(NoneSource)
