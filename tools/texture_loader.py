import bpy
import os
from ..material_class import Material
from .global_tools import Tools
from .place_nodes import *

__all__ = ['GetTextureOperator', 'AutoHook']


class GetTextureOperator(bpy.types.Operator):
    bl_idname = "pbr.get_textures_op"
    bl_label = "Assign Textures"
    bl_description = "Assign files with textures using chosen name pattern"

    reloaded_images = 0

    @staticmethod
    def execute(self, context):
        path = context.active_object.active_material.props.textures_path
        filenames = next(os.walk(path), (None, None, []))[2]
        GetTextureOperator.reloaded_images = 0

        clear_material()
        Material.MATERIALS['CURRENT'].reset()
        [GetTextureOperator.get_texture(file) for file in filenames]
        textures = Material.MATERIALS['CURRENT']
        if any(textures.found_textures.values()):
            Material.MATERIALS['CURRENT'].finished = True
            place_automatic()
            if 'UVMap' not in context.object.active_material.node_tree.nodes:
                self.report({'WARNING'}, Tools.MESSAGES["UV_Warning"])
            else:
                if GetTextureOperator.reloaded_images:
                    message = f'Loading finished with {GetTextureOperator.reloaded_images} ' \
                              f'{"image" if GetTextureOperator.reloaded_images == 1 else "images"} ' \
                              'reloaded from blendfile'
                    self.report({'INFO'}, message)
                else:
                    self.report({'INFO'}, Tools.MESSAGES["Texture_Getter_Success"])
        else:
            self.report({'WARNING'}, Tools.MESSAGES["Texture_Getter_Warning"])

        [bpy.data.images.remove(image) for image in bpy.data.images
         if image.users == 0
         and image.name != 'Viewer Node'
         and image not in Material.used_images()]

        return {"FINISHED"}

    @staticmethod
    def get_texture(file):
        if file.lower().split(".")[-1] == 'meta':
            return
        else:
            splitter = file.lower().split(".")
            name = ".".join(splitter[:-1]) if len(splitter) > 2 else splitter[0]
            
        names = bpy.context.active_object.active_material.props.textures_pattern.lower().split("-")
        pattern = names[0].strip()

        if len(names) > 1:
            skip_names = list(map(str.strip, names[1:]))
            if any(stop_word in name for stop_word in skip_names):
                return

        if pattern not in name:
            return
        
        is_tile = False
        threshold = 0
        title = ''

        if name[-4:].isnumeric():
            is_tile = True
            tile_number = int(name[-4:])
            if file.replace(str(tile_number), '1001') in bpy.data.images.keys():
                if tile_number != 1001:
                    bpy.data.images[file.replace(str(tile_number), '1001')].tiles.new(tile_number)
                    return
            else:
                name = name[:name.index(str(tile_number))-1]

        for texture in Tools.TEXTURE_TYPES:
            if Material.MATERIALS['CURRENT'].found_textures[texture]:
                continue
            for mask in Tools.TEXTURES_KEYWORDS_DICT[texture]:
                if name.endswith(mask):
                    if len(mask) > threshold:
                        threshold = len(mask)
                        title = texture
                        continue

        if threshold != 0:
            new_image_path = os.path.join(bpy.context.active_object.active_material.props.textures_path, file)
            if file in bpy.data.images.keys() and bpy.data.images[file].filepath == new_image_path:
                bpy.data.images[file].reload()
                image = bpy.data.images[file]
                GetTextureOperator.reloaded_images += 1
            else:
                image = bpy.data.images.load(filepath=new_image_path)
            if is_tile:
                image.source = 'TILED'
            image.colorspace_settings.name = Tools.TEXTURES_COLORING[title]
            Material.MATERIALS['CURRENT'].found_textures[title] = True
            Material.MATERIALS['CURRENT'].images[title] = image


class AutoHook(bpy.types.Operator):
    bl_idname = "pbr.auto_hook_op"
    bl_label = "AutoHook"
    bl_description = "Automatically hook all materials. \nNOTE: It makes all materials use shared path and use material name as a material keyword!"

    @staticmethod
    def execute(self, context):
        bpy.ops.pbr.set_path_shared()
        materials = bpy.context.active_object.material_slots
        for mat in materials:
            mat.material.props.UseMaterialNameAsKeyword = True
            mat.material.props.textures_pattern = mat.material.name
        for i in range(len(materials)):
            bpy.context.active_object.active_material_index = i
            Material.MATERIALS['CURRENT'] = Material.MATERIALS[materials[i].material.name]
            bpy.ops.pbr.get_textures_op()

        return {"FINISHED"}

def register():
    bpy.utils.register_class(AutoHook)
    bpy.utils.register_class(GetTextureOperator)


def unregister():
    bpy.utils.unregister_class(AutoHook)
    bpy.utils.unregister_class(GetTextureOperator)
