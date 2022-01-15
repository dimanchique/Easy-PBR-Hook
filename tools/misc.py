import bpy

__all__ = ['TEXTURES_MASK', 'TEXTURES']


def read_texture_masks():
    textures = {}
    with open(bpy.utils.user_resource('SCRIPTS', "addons") + '\\Easy-PBR-Hook-multifile_beta\\tools\\mask.dat', 'r') as file:
        masks = file.readlines()
    for line in masks:
        key = line.split(':')[0]
        textures[key] = tuple(''.join(line.strip().split(':')[1:]).replace(" ", "").split(','))
    print(textures)
    return textures


TEXTURES_MASK = read_texture_masks()


TEXTURES = list(TEXTURES_MASK.keys())
