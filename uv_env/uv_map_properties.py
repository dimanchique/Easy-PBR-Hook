import bpy

__all__ = ['UVMapProp', 'uv_items', 'register', 'unregister']


class UVMapProp(bpy.types.PropertyGroup):
    uv: bpy.props.StringProperty()


def uv_items(self, context):
    enum_items = []
    for UV in bpy.data.meshes[context.active_object.data.name].uv_layers.keys():
        data = str(UV)
        item = (data, data, '')
        enum_items.append(item)
    return enum_items


def register():
    bpy.utils.register_class(UVMapProp)


def unregister():
    bpy.utils.unregister_class(UVMapProp)