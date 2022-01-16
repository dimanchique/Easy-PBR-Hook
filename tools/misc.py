import bpy
import os

__all__ = ['TEXTURES_MASK', 'TEXTURES']


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
