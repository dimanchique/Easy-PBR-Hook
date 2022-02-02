import bpy
import os
from ..material_class import Material
from .global_tools import Tools
from .place_nodes import *

__all__ = ['GetTextureOperator']


class GetTextureOperator(bpy.types.Operator):
    bl_idname = "pbr.get_textures_op"
    bl_label = "Assign Textures"
    bl_description = "Assign files with textures using chosen name pattern"

    reloaded_images = 0

    @staticmethod
    def execute(self, context):
        GetTextureOperator.reloaded_images = 0
        clear_material()
        Material.MATERIALS['CURRENT'].reset()
        path = context.active_object.active_material.props.textures_path
        filenames = next(os.walk(path), (None, None, []))[2]
        [GetTextureOperator.get_texture(file) for file in filenames]
        textures = Material.MATERIALS['CURRENT']
        if any(textures.found[texture] for texture in textures.found):
            Material.MATERIALS['CURRENT'].finished = True
            place_automatic()
            if 'UVMap' not in context.object.active_material.node_tree.nodes:
                self.report({'WARNING'}, Tools.UV_MAP_WARNING_MESSAGE)
            else:
                if GetTextureOperator.reloaded_images:
                    ending = 'image' if GetTextureOperator.reloaded_images == 1 else 'images'
                    message = f'Loading finished with {GetTextureOperator.reloaded_images} ' \
                              f'{ending} reloaded from blendfile'
                    self.report({'INFO'}, message)
                else:
                    self.report({'INFO'}, Tools.SUCCESS_LOADING)
        else:
            self.report({'WARNING'}, Tools.TEXTURE_GETTER_WARNING_MESSAGE)

        [bpy.data.images.remove(image) for image in bpy.data.images
         if image.users == 0
         and image.name != 'Viewer Node'
         and image not in list(Material.MATERIALS['CURRENT'].images.values())]

        return {"FINISHED"}

    @staticmethod
    def get_texture(file):
        is_tile = False
        threshold = 0
        title = ''

        name = file.lower().split(".")[0]
        if name.split('_')[-1].isnumeric():
            is_tile = True
            tile_number = int(name.split('_')[-1])
            if file.replace(str(tile_number), '1001') in bpy.data.images.keys():
                if tile_number != 1001:
                    bpy.data.images[file.replace(str(tile_number), '1001')].tiles.new(tile_number)
                    return
            name = name.replace(f'_{tile_number}', '')
        pattern = bpy.context.active_object.active_material.props.textures_pattern.lower().split("-")
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

        for texture in Tools.TEXTURES:
            if Material.MATERIALS['CURRENT'].found[texture]:
                continue
            for mask in Tools.TEXTURES_MASK[texture]:
                if name.endswith(mask.lower()):
                    if len(mask.lower()) > threshold:
                        threshold = len(mask.lower())
                        title = texture
                        break

        if threshold != 0:
            if file in bpy.data.images.keys():
                bpy.data.images[file].reload()
                image = bpy.data.images[file]
                GetTextureOperator.reloaded_images += 1
            else:
                image = bpy.data.images.load(
                    filepath=os.path.join(bpy.context.active_object.active_material.props.textures_path, file))
            if is_tile:
                image.source = 'TILED'
            image.colorspace_settings.name = Tools.TEXTURES_COLORS[title]
            Material.MATERIALS['CURRENT'].found[title] = True
            Material.MATERIALS['CURRENT'].images[title] = image


def register():
    bpy.utils.register_class(GetTextureOperator)


def unregister():
    bpy.utils.unregister_class(GetTextureOperator)
