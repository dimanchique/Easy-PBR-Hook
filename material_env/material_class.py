import bpy
from ..tools.misc import *

__all__ = ['Material', 'get_mode', 'add_to_nodes_list']


class Material:
    MATERIALS = {}

    def __init__(self, name):
        self.name = name
        Material.MATERIALS[name] = self
        Material.MATERIALS['CURRENT'] = self
        self.current_path = ''
        self.current_pattern = ''
        self.found = dict.fromkeys(TEXTURES, False)
        self.images = dict.fromkeys(TEXTURES, None)
        self.nodes_list = []
        self.opacity_mode = "Opaque"
        self.opacity_from_albedo = False
        self.finished = False
        self.automatic = True
        self.mask_source = "Detail Mask"

    def reset(self):
        self.found = dict.fromkeys(TEXTURES, False)
        self.images = dict.fromkeys(TEXTURES, None)
        self.finished = False
        self.automatic = True
        self.soft_reset()
        bpy.context.object.active_material.blend_method = "OPAQUE"
        bpy.context.object.active_material.shadow_method = "OPAQUE"

    def soft_reset(self):
        self.nodes_list = []
        self.opacity_mode = "Opaque"
        self.opacity_from_albedo = False
        self.mask_source = "Detail Mask"


def get_mode():
    return f"Mode: {' + '.join(Material.MATERIALS['CURRENT'].nodes_list)} " \
           f"({'Automatic' if Material.MATERIALS['CURRENT'].automatic else 'Manual'})"


def add_to_nodes_list(mode):
    if mode not in Material.MATERIALS['CURRENT'].nodes_list:
        Material.MATERIALS['CURRENT'].nodes_list.append(mode)
