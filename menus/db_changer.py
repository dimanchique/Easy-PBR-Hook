import bpy
import os
from ..tools.misc import TEXTURES, TEXTURES_MASK

__all__ = ['DBChanger']


class DBChanger(bpy.types.Operator):
    bl_idname = "pbr.dbchanger"
    bl_label = "Change texture masks database"
    bl_description = "Add specific endings of your textures for every type of textures"

    properties_list = ['albedo', 'met_sm', 'metal', 'rough', 'orm', 'color_mask',
                       'normal_map', 'emission', 'specular', 'occlusion',
                       'displacement', 'opacity', 'detail_map', 'detail_mask']

    matching = dict(zip(properties_list, TEXTURES))

    @staticmethod
    def execute(self, context):
        if context.active_object.active_material.db_strings.Update == 'Local':
            local_update()
        elif context.active_object.active_material.db_strings.Update == 'Global':
            global_update()
        self.report({'INFO'}, "Database was updated!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        for prop in DBChanger.properties_list:
            row = layout.row()
            row.prop(context.active_object.active_material.db_strings, prop)
        row = layout.row()
        row.prop(context.active_object.active_material.db_strings, 'Update')


def local_update():
    matching = DBChanger.matching
    data = dict(bpy.context.active_object.active_material.db_strings.items())
    for item in matching:
        if item in data:
            line = list(data[item].strip().replace(" ", "").split(','))
            line = [i for i in line if i != '']
            TEXTURES_MASK[matching[item]] = tuple(set(line))
#    for item in bpy.context.active_object.active_material.db_strings.items():
#        if item[0] in matching:
#            TEXTURES_MASK[matching[item[0]]] = tuple(list(TEXTURES_MASK[matching[item[0]]]) +
#                                                     list(item[1].strip().replace(" ", "").split(',')))


def global_update():
    local_update()
    data = []
    for i in TEXTURES_MASK:
        data.append(f'{i}: {", ".join(TEXTURES_MASK[i])}\n')
    path = os.path.dirname(os.path.realpath(__file__))
    path = '\\'.join(path.split('\\')[:-1])+'\\tools'
    with open(path + '\\mask.dat', 'w') as file:
        file.write(''.join(data))


def register():
    bpy.utils.register_class(DBChanger)


def unregister():
    bpy.utils.unregister_class(DBChanger)
