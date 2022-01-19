import os

__all__ = ['TEXTURES_MASK', 'TEXTURES', 'TEXTURES_COLORS', 'UV_MAP_WARNING_MESSAGE',
           'TEXTURE_GETTER_WARNING_MESSAGE', 'GLOBAL_UPDATE', 'LOCAL_UPDATE', 'IMAGE_UPDATE']


def read_texture_masks():
    textures = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\mask.dat', 'r') as file:
        masks = file.readlines()
    for line in masks:
        key = line.split(':')[0]
        data = line.split(':')[1]
        textures[key] = tuple(map(str.strip, data.split(',')))
    return textures


TEXTURES_MASK = read_texture_masks()

TEXTURES = list(TEXTURES_MASK.keys())


# STRING MESSAGES
UV_MAP_WARNING_MESSAGE = 'UV Map not found. Please, fix this problem to use Texture coordinates section!'
TEXTURE_GETTER_WARNING_MESSAGE = 'No textures found! Check path and keyword.'
GLOBAL_UPDATE = "Database was globally updated!"
LOCAL_UPDATE = "Database was locally updated!"
IMAGE_UPDATE = "Images were updated!"


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
