import bpy
from ..tools.global_tools import Tools

__all__ = ['DataBaseProps']


class DataBaseProps(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.db_strings = bpy.props.PointerProperty(name="Custom properties",
                                                               description="Custom Properties for textures Database",
                                                               type=cls)
        cls.albedo = bpy.props.StringProperty(name="Albedo",
                                              description="Albedo keyword",
                                              default=', '.join(Tools.TEXTURES_MASK['Albedo']))
        cls.met_sm = bpy.props.StringProperty(name="Metal Smoothness",
                                              description="Metal Smoothness keyword",
                                              default=', '.join(Tools.TEXTURES_MASK['Metal Smoothness']))
        cls.metal = bpy.props.StringProperty(name="Metal",
                                             description="Metal keyword",
                                             default=', '.join(Tools.TEXTURES_MASK['Metal']))
        cls.rough = bpy.props.StringProperty(name="Roughness",
                                             description="Roughness keyword",
                                             default=', '.join(Tools.TEXTURES_MASK['Roughness']))
        cls.orm = bpy.props.StringProperty(name="ORM",
                                           description="ORM keyword",
                                           default=', '.join(Tools.TEXTURES_MASK['ORM']))
        cls.color_mask = bpy.props.StringProperty(name="Color Mask",
                                                  description="Color Mask keyword",
                                                  default=', '.join(Tools.TEXTURES_MASK['Color Mask']))
        cls.normal_map = bpy.props.StringProperty(name="Normal Map",
                                                  description="Normal Map keyword",
                                                  default=', '.join(Tools.TEXTURES_MASK['Normal Map']))
        cls.emission = bpy.props.StringProperty(name="Emission",
                                                description="Emission keyword",
                                                default=', '.join(Tools.TEXTURES_MASK['Emission']))
        cls.specular = bpy.props.StringProperty(name="Specular",
                                                description="Specular keyword",
                                                default=', '.join(Tools.TEXTURES_MASK['Specular']))
        cls.occlusion = bpy.props.StringProperty(name="Occlusion",
                                                 description="Occlusion keyword",
                                                 default=', '.join(Tools.TEXTURES_MASK['Occlusion']))
        cls.displacement = bpy.props.StringProperty(name="Displacement",
                                                    description="Displacement keyword",
                                                    default=', '.join(Tools.TEXTURES_MASK['Displacement']))
        cls.opacity = bpy.props.StringProperty(name="Opacity",
                                               description="Opacity keyword",
                                               default=', '.join(Tools.TEXTURES_MASK['Opacity']))
        cls.detail_map = bpy.props.StringProperty(name="Detail Map",
                                                  description="Detail Map keyword",
                                                  default=', '.join(Tools.TEXTURES_MASK['Detail Map']))
        cls.detail_mask = bpy.props.StringProperty(name="Detail Mask",
                                                   description="Detail Mask",
                                                   default=', '.join(Tools.TEXTURES_MASK['Detail Mask']))

        cls.Update = bpy.props.EnumProperty(items=[('Local', 'Local', ''),
                                                   ('Global', 'Global', '')])


def register():
    bpy.utils.register_class(DataBaseProps)


def unregister():
    bpy.utils.unregister_class(DataBaseProps)
