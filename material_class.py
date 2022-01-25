import bpy
from .tools.global_tools import Tools

__all__ = ['Material']


class Material:
    MATERIALS = {}

    if not Tools.TEXTURES:
        Tools.update_files()

    def __init__(self, name):
        self.name = name
        Material.MATERIALS[name] = self
        Material.MATERIALS['CURRENT'] = self
        self.current_path = ''
        self.current_pattern = ''
        self.found = dict.fromkeys(Tools.TEXTURES, False)
        self.images = dict.fromkeys(Tools.TEXTURES, None)
        self.nodes_list = []
        self.opacity_mode = "Opaque"
        self.opacity_from_albedo = False
        self.finished = False
        self.automatic = True
        self.mask_source = "Detail Mask"

    def reset(self):
        self.found = dict.fromkeys(Tools.TEXTURES, False)
        self.images = dict.fromkeys(Tools.TEXTURES, None)
        self.finished = False
        self.automatic = True
        self.soft_reset()

    def soft_reset(self):
        self.nodes_list = []
        self.opacity_mode = "Opaque"
        bpy.context.object.active_material.blend_method = "OPAQUE"
        bpy.context.object.active_material.shadow_method = "OPAQUE"
        self.mask_source = "Detail Mask"
        self.opacity_from_albedo = False

    @classmethod
    def check_material(cls, material_name):
        if 'CURRENT' not in cls.MATERIALS:
            cls(material_name)
        elif cls.MATERIALS['CURRENT'].name != material_name:
            if material_name not in cls.MATERIALS:
                cls(material_name)
            else:
                cls.MATERIALS['CURRENT'] = cls.MATERIALS[material_name]

    @classmethod
    def get_material_mode(cls):
        text = 'Mode: '
        if not cls.MATERIALS['CURRENT'].nodes_list:
            return text + "None"
        else:
            return text + f"{' + '.join(cls.MATERIALS['CURRENT'].nodes_list)} " \
                          f"({'Automatic' if cls.MATERIALS['CURRENT'].automatic else 'Manual'})"

    @classmethod
    def add_to_nodes_list(cls, node):
        if node not in cls.MATERIALS['CURRENT'].nodes_list:
            cls.MATERIALS['CURRENT'].nodes_list.append(node)

    @classmethod
    def remove_from_nodes_list(cls, node):
        if node in cls.MATERIALS['CURRENT'].nodes_list:
            cls.MATERIALS['CURRENT'].nodes_list.remove(node)

    @classmethod
    def pipelines_found(cls):
        return cls.MATERIALS['CURRENT'].found["ORM"] \
            or cls.MATERIALS['CURRENT'].found["Metal Smoothness"] \
            or cls.MATERIALS['CURRENT'].found["Metal"] \
            or cls.MATERIALS['CURRENT'].found["Roughness"]
