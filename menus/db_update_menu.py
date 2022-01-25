import bpy
from ..tools.global_tools import Tools, DataExporter, DataImporter

__all__ = ['DBUpdateMenu']


class DBUpdateMenu(bpy.types.Operator):
    bl_idname = "pbr.db_update"
    bl_label = "Change texture masks database"
    bl_description = "Add specific endings of your textures for every type of textures"

    @staticmethod
    def execute(self, context):
        if context.scene.db_strings.Update == 'Local':
            Tools.local_update()
        elif context.scene.db_strings.Update == 'Global':
            Tools.global_update()
        self.report({'INFO'}, Tools.UPDATE_DATABASE[context.scene.db_strings.Update])
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=700)

    def draw(self, context):
        layout = self.layout
        for prop in Tools.PROP_TO_TEXTURE:
            row = layout.row()
            row.prop(context.scene.db_strings, prop)
        row = layout.row()
        row.operator(DataExporter.bl_idname)
        sub = row.row()
        sub.operator(DataImporter.bl_idname)
        row = layout.row()
        row.prop(context.scene.db_strings, 'Update')


def register():
    bpy.utils.register_class(DBUpdateMenu)


def unregister():
    bpy.utils.unregister_class(DBUpdateMenu)
