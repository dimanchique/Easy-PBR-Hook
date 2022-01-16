import bpy
from ..material_env.material_class import Material

__all__ = ['DetailMapCoordinatesPanel']


class DetailMapCoordinatesPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_DetailMapCoordinates"
    bl_space_type = "PROPERTIES"
    bl_label = "Detail Map Coordinates"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return Material.MATERIALS['CURRENT'].finished and context.active_object.active_material is not None and \
            "Detail Mapping" in context.object.active_material.node_tree.nodes

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        layout = self.layout
        for prop in ["DetailMapLocation", "DetailMapRotation", "DetailMapScale"]:
            row = layout.row()
            row.prop(material_prop, prop)


def register():
    bpy.utils.register_class(DetailMapCoordinatesPanel)


def unregister():
    bpy.utils.unregister_class(DetailMapCoordinatesPanel)
