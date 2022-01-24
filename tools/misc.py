import os
import json

__all__ = ['TEXTURES_MASK', 'TEXTURES', 'TEXTURES_COLORS', 'PROP_TO_TEXTURE', 'UV_MAP_WARNING_MESSAGE',
           'TEXTURE_GETTER_WARNING_MESSAGE', 'GLOBAL_UPDATE', 'LOCAL_UPDATE', 'IMAGE_UPDATE',
           'DETAIL_MASK_PLACED', 'DETAIL_MASK_REMOVED']

with open(os.path.dirname(os.path.realpath(__file__)) + '\\texture_mask.json', 'r') as file:
    TEXTURES_MASK = json.load(file)
    TEXTURES = list(TEXTURES_MASK.keys())

with open(os.path.dirname(os.path.realpath(__file__)) + '\\texture_colors.json', 'r') as file:
    TEXTURES_COLORS = json.load(file)

with open(os.path.dirname(os.path.realpath(__file__)) + '\\prop_to_texture_match.json', 'r') as file:
    PROP_TO_TEXTURE = json.load(file)

# MESSAGES
UV_MAP_WARNING_MESSAGE = 'UV Map not found. Please, fix this problem to use Texture coordinates section!'
TEXTURE_GETTER_WARNING_MESSAGE = 'No textures found! Check path and keyword'
GLOBAL_UPDATE = "Database was globally updated!"
LOCAL_UPDATE = "Database was locally updated!"
IMAGE_UPDATE = "Images were updated!"
DETAIL_MASK_PLACED = 'Detail Mask node was created'
DETAIL_MASK_REMOVED = 'Detail Mask node was removed'
