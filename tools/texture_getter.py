import bpy
import os
from ..material_class import Material
from .misc import *
from .place_funcs import *

__all__ = ['GetTextureOperator']


class GetTextureOperator(bpy.types.Operator):
    bl_idname = "pbr.get_textures_op"
    bl_label = "Assign Textures"
    bl_description = "Assign files with textures using chosen name pattern"

    @staticmethod
    def execute(self, context):
        clear_images()
        Material.MATERIALS['CURRENT'].reset()
        path = context.active_object.active_material.props.textures_path
        filenames = next(os.walk(path), (None, None, []))[2]
        [GetTextureOperator.get_texture(file) for file in filenames]
        textures = Material.MATERIALS['CURRENT']
        if any(textures.found[texture] for texture in textures.found):
            Material.MATERIALS['CURRENT'].finished = True
            place_automatic()
            if 'UVMap' not in context.object.active_material.node_tree.nodes:
                self.report({'WARNING'}, UV_MAP_WARNING_MESSAGE)
        else:
            self.report({'WARNING'}, TEXTURE_GETTER_WARNING_MESSAGE)
        return {"FINISHED"}

    @staticmethod
    def get_texture(file):
        threshold = 0
        title = ''

        if file.split(".")[-1].lower() == 'meta':
            return False

        name = file.lower().split(".")[0]
        pattern = bpy.context.active_object.active_material.props.textures_pattern.lower().split("-")

        if len(pattern) > 1:
            pattern, skip = pattern[0].strip(), pattern[1].strip()
        else:
            pattern, skip = pattern[0].strip(), None
        if skip is not None and skip in name:
            return False

        for texture in TEXTURES:
            for mask in TEXTURES_MASK[texture]:
                if name.endswith(mask.lower()):
                    if len(mask.lower()) > threshold:
                        threshold = len(mask.lower())
                        title = texture
                        break

        if threshold != 0 and pattern in name:
            if file in bpy.data.images:
                bpy.data.images.remove(bpy.data.images[file])
            image = bpy.data.images.load(
                filepath=os.path.join(bpy.context.active_object.active_material.props.textures_path, file))

            image.colorspace_settings.name = TEXTURES_COLORS[title]
            Material.MATERIALS['CURRENT'].found[title] = True
            Material.MATERIALS['CURRENT'].images[title] = image
        return True


def register():
    bpy.utils.register_class(GetTextureOperator)


def unregister():
    bpy.utils.unregister_class(GetTextureOperator)
