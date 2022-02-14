import bpy
from ..tools.global_tools import Tools, DataExporter, DataImporter

__all__ = ['DBUpdateMenu']


class DBUpdateMenu(bpy.types.Operator):
    bl_idname = "pbr.db_update"
    bl_label = "Change texture masks database"
    bl_description = "Add specific endings of your textures for every type of textures"

    @staticmethod
    def execute(self, context):
        update_type = context.scene.db_strings.Update
        if update_type == 'Local' or update_type == 'Global':
            if update_type == 'Local':
                Tools.local_update()
            else:
                Tools.global_update()
            self.report({'INFO'}, Tools.MESSAGES["Database_Update_Success"][update_type])
        else:
            self.report({'INFO'}, Tools.MESSAGES["Database_Update_Error"])
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        layout = self.layout
        for prop in Tools.PROP_TO_TEXTURE:
            row = layout.row()
            row.prop(context.scene.db_strings, prop)
        row = layout.row()
        row.prop(context.scene.db_strings, 'Update')
        row = layout.row()
        row.operator(DataExporter.bl_idname)
        row.operator(DataImporter.bl_idname)


def register():
    bpy.utils.register_class(DBUpdateMenu)


def unregister():
    bpy.utils.unregister_class(DBUpdateMenu)
