import os

__all__ = ['TEXTURES_MASK', 'TEXTURES', 'TEXTURES_COLORS', 'UV_MAP_WARNING_MESSAGE', 'TEXTURE_GETTER_WARNING_MESSAGE']


def read_texture_masks():
    textures = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\mask.dat', 'r') as file:
        masks = file.readlines()
    for line in masks:
        key = line.split(':')[0]
        textures[key] = tuple(''.join(line.strip().split(':')[1:]).replace(" ", "").split(','))
    return textures


TEXTURES_MASK = read_texture_masks()

TEXTURES = list(TEXTURES_MASK.keys())

UV_MAP_WARNING_MESSAGE = 'UV Map not found. Please, fix this problem to use Texture coordinates section!'
TEXTURE_GETTER_WARNING_MESSAGE = 'No textures found! Check path and keyword'

TEXTURES_COLORS = {'Albedo': 'sRGB',
                   'Metal Smoothness': 'Non-Color',
                   'Metal': 'Non-Color',
                   'Roughness': 'Non-Color',
                   'ORM': 'Non-Color',
                   'Color Mask': 'Non-Color',
                   'Normal Map': 'Non-Color',
                   'Emission': 'sRGB',
                   'Specular': 'sRGB',
                   'Occlusion': 'sRGB',
                   'Displacement': 'Non-Color',
                   'Opacity': 'Non-Color',
                   'Detail Map': 'Non-Color',
                   'Detail Mask': 'Non-Color'
                   }
