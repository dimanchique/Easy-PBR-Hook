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
                                              default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Albedo']))
        cls.met_sm = bpy.props.StringProperty(name="Metal Smoothness",
                                              description="Metal Smoothness keyword",
                                              default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Metal Smoothness']))
        cls.metal = bpy.props.StringProperty(name="Metal",
                                             description="Metal keyword",
                                             default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Metal']))
        cls.rough = bpy.props.StringProperty(name="Roughness",
                                             description="Roughness keyword",
                                             default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Roughness']))
        cls.orm = bpy.props.StringProperty(name="ORM",
                                           description="ORM keyword",
                                           default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['ORM']))
        cls.color_mask = bpy.props.StringProperty(name="Color Mask",
                                                  description="Color Mask keyword",
                                                  default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Color Mask']))
        cls.normal_map = bpy.props.StringProperty(name="Normal Map",
                                                  description="Normal Map keyword",
                                                  default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Normal Map']))
        cls.emission = bpy.props.StringProperty(name="Emission",
                                                description="Emission keyword",
                                                default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Emission']))
        cls.specular = bpy.props.StringProperty(name="Specular",
                                                description="Specular keyword",
                                                default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Specular']))
        cls.occlusion = bpy.props.StringProperty(name="Occlusion",
                                                 description="Occlusion keyword",
                                                 default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Occlusion']))
        cls.displacement = bpy.props.StringProperty(name="Displacement",
                                                    description="Displacement keyword",
                                                    default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Displacement']))
        cls.opacity = bpy.props.StringProperty(name="Opacity",
                                               description="Opacity keyword",
                                               default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Opacity']))
        cls.detail_map = bpy.props.StringProperty(name="Detail Map",
                                                  description="Detail Map keyword",
                                                  default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Detail Map']))
        cls.detail_mask = bpy.props.StringProperty(name="Detail Mask",
                                                   description="Detail Mask",
                                                   default=', '.join(Tools.TEXTURES_KEYWORDS_DICT['Detail Mask']))

        cls.Update = bpy.props.EnumProperty(items=[('Local', 'Local', ''),
                                                   ('Global', 'Global', '')])


def register():
    bpy.utils.register_class(DataBaseProps)


def unregister():
    bpy.utils.unregister_class(DataBaseProps)
