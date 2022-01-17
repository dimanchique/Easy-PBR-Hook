import bpy
import os
from ..tools.misc import TEXTURES, TEXTURES_MASK

__all__ = ['DBUpdateMenu']


class DBUpdateMenu(bpy.types.Operator):
    bl_idname = "pbr.db_update"
    bl_label = "Change texture masks database"
    bl_description = "Add specific endings of your textures for every type of textures"

    properties_list = ['albedo', 'met_sm', 'metal', 'rough', 'orm', 'color_mask',
                       'normal_map', 'emission', 'specular', 'occlusion',
                       'displacement', 'opacity', 'detail_map', 'detail_mask']

    matching = dict(zip(properties_list, TEXTURES))

    @staticmethod
    def execute(self, context):
        if context.scene.db_strings.Update == 'Local':
            local_update()
        elif context.scene.db_strings.Update == 'Global':
            global_update()
        self.report({'INFO'}, "Database was updated!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        layout = self.layout
        for prop in DBUpdateMenu.properties_list:
            row = layout.row()
            row.prop(context.scene.db_strings, prop)
        row = layout.row()
        row.prop(context.scene.db_strings, 'Update')


def local_update():
    matching = DBUpdateMenu.matching
    data = dict(bpy.context.scene.db_strings.items())
    for item in matching:
        if item in data:
            line = list(data[item].strip().replace(" ", "").split(','))
            line = [i for i in line if i != '']
            TEXTURES_MASK[matching[item]] = tuple(set(line))


def global_update():
    local_update()
    data = [f'{i}: {", ".join(TEXTURES_MASK[i])}\n' for i in TEXTURES_MASK]
    # Step up to main dir and step into tools
    path = '\\'.join(os.path.dirname(os.path.realpath(__file__)).split('\\')[:-1])+'\\tools\\mask.dat'
    with open(path, 'w') as file:
        file.write(''.join(data))


def register():
    bpy.utils.register_class(DBUpdateMenu)


def unregister():
    bpy.utils.unregister_class(DBUpdateMenu)
