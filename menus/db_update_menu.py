import bpy
import os
import json
from ..tools.misc import TEXTURES_MASK, PROP_TO_TEXTURE, UPDATE_DATABASE

__all__ = ['DBUpdateMenu']


class DBUpdateMenu(bpy.types.Operator):
    bl_idname = "pbr.db_update"
    bl_label = "Change texture masks database"
    bl_description = "Add specific endings of your textures for every type of textures"

    @staticmethod
    def execute(self, context):
        if context.scene.db_strings.Update == 'Local':
            local_update()
        elif context.scene.db_strings.Update == 'Global':
            global_update()
        self.report({'INFO'}, UPDATE_DATABASE[context.scene.db_strings.Update])
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=700)

    def draw(self, context):
        layout = self.layout
        for prop in PROP_TO_TEXTURE:
            row = layout.row()
            row.prop(context.scene.db_strings, prop)
        row = layout.row()
        row.prop(context.scene.db_strings, 'Update')


def local_update():
    data = dict(bpy.context.scene.db_strings.items())
    for item in data:
        if item in PROP_TO_TEXTURE:
            line = list(map(str.strip, data[item].split(',')))
            line = [i for i in line if i != '']
            TEXTURES_MASK[PROP_TO_TEXTURE[item]] = list(set(line))


def global_update():
    local_update()
    path = '\\'.join(os.path.dirname(os.path.realpath(__file__)).split('\\')[:-1])+'\\tools\\texture_mask.json'
    with open(path, 'w') as file:
        json.dump(TEXTURES_MASK, file)


def register():
    bpy.utils.register_class(DBUpdateMenu)


def unregister():
    bpy.utils.unregister_class(DBUpdateMenu)
