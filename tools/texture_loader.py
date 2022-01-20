import bpy
import os
from ..material_class import Material
from .misc import *
from .place_nodes import *

__all__ = ['GetTextureOperator']


class GetTextureOperator(bpy.types.Operator):
    bl_idname = "pbr.get_textures_op"
    bl_label = "Assign Textures"
    bl_description = "Assign files with textures using chosen name pattern"

    @staticmethod
    def execute(self, context):
        clear_images()
        clear_material()
        Material.MATERIALS['CURRENT'].reset()
        path = context.active_object.active_material.props.textures_path
        filenames = next(os.walk(path), (None, None, []))[2]
        [GetTextureOperator.get_texture(context, file) for file in filenames]
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
    def get_texture(context, file):
        threshold = 0
        title = ''
        
        name = file.lower().split(".")[0]
        pattern = context.active_object.active_material.props.textures_pattern.lower().split("-")
        skip_names = None
        
        if len(pattern) > 1:
            pattern, skip_names = pattern[0].strip(), list(map(str.strip, pattern[1:]))
        else:
            pattern = pattern[0].strip()

        if file.split(".")[-1].lower() == 'meta' or \
                pattern not in name or \
                (skip_names is not None and
                 any(stop_word in name for stop_word in skip_names)):
            return 

        for texture in TEXTURES:
            for mask in TEXTURES_MASK[texture]:
                if name.endswith(mask.lower()):
                    if len(mask.lower()) > threshold:
                        threshold = len(mask.lower())
                        title = texture
                        break

        if threshold != 0:
            if file in bpy.data.images:
                bpy.data.images.remove(bpy.data.images[file])
            image = bpy.data.images.load(
                filepath=os.path.join(bpy.context.active_object.active_material.props.textures_path, file))

            image.colorspace_settings.name = TEXTURES_COLORS[title]
            Material.MATERIALS['CURRENT'].found[title] = True
            Material.MATERIALS['CURRENT'].images[title] = image
        return


def register():
    bpy.utils.register_class(GetTextureOperator)


def unregister():
    bpy.utils.unregister_class(GetTextureOperator)
