import bpy
from ..tools.update_tool import *
from ..uv_env.uv_map_properties import UVMapProp, uv_items

__all__ = ['MaterialProps']


class MaterialProps(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Material.props = bpy.props.PointerProperty(name="Custom properties",
                                                             description="Custom Properties for Material",
                                                             type=cls)
########################################################################################################################
# FLOAT PROPERTIES
########################################################################################################################
        cls.RoughnessAdd = bpy.props.FloatProperty(name="Roughness",
                                                   min=0,
                                                   max=1,
                                                   update=lambda a, b:
                                                   update_float(a, b, "Roughness"))

        cls.MetallicAdd = bpy.props.FloatProperty(name="Metallic",
                                                  min=0,
                                                  max=1,
                                                  update=lambda a, b:
                                                  update_float(a, b, "Metallic"))

        cls.SpecularAdd = bpy.props.FloatProperty(name="Specular",
                                                  min=0,
                                                  max=100,
                                                  update=lambda a, b:
                                                  update_float(a, b, "Specular"))

        cls.EmissionMult = bpy.props.FloatProperty(name="Emission",
                                                   min=0,
                                                   max=1,
                                                   update=lambda a, b:
                                                   update_float(a, b, "Emission"))

        cls.NormaMapStrength = bpy.props.FloatProperty(name="Normal Strength",
                                                       min=0,
                                                       update=lambda a, b:
                                                       update_float(a, b, "Normal Strength"))

        cls.AO_Strength = bpy.props.FloatProperty(name="AO Strength",
                                                  min=0,
                                                  max=1,
                                                  update=lambda a, b:
                                                  update_float(a, b, "AO Strength"))

        cls.AlphaThreshold = bpy.props.FloatProperty(name="Alpha Threshold",
                                                     min=0,
                                                     max=1,
                                                     update=lambda a, b:
                                                     update_float(a, b, "Alpha Threshold"))

        cls.DetailMaskStrength = bpy.props.FloatProperty(name="Detail Mask Strength",
                                                         min=0,
                                                         max=1,
                                                         update=lambda a, b:
                                                         update_float(a, b, "Detail Mask Strength"))

        cls.OpacityAdd = bpy.props.FloatProperty(name="Opacity",
                                                 min=0,
                                                 max=1,
                                                 update=lambda a, b:
                                                 update_float(a, b, "Opacity"))
########################################################################################################################
# BOOLEAN PROPERTIES
########################################################################################################################
        cls.NormalMapInverterEnabled = bpy.props.BoolProperty(name="Invert Normal",
                                                              update=update_normal)

        cls.DetailMapInverterEnabled = bpy.props.BoolProperty(name="Invert Detail",
                                                              update=update_detail)
########################################################################################################################
# FLOAT VECTOR PROPERTIES (COLORS)
########################################################################################################################
        cls.MixR = bpy.props.FloatVectorProperty(name="Red channel",
                                                 subtype="COLOR",
                                                 size=4,
                                                 min=0,
                                                 max=1,
                                                 update=update_color)

        cls.MixG = bpy.props.FloatVectorProperty(name="Green channel",
                                                 subtype="COLOR",
                                                 size=4,
                                                 min=0,
                                                 max=1,
                                                 update=update_color)

        cls.MixB = bpy.props.FloatVectorProperty(name="Blue channel",
                                                 subtype="COLOR",
                                                 size=4,
                                                 min=0,
                                                 max=1,
                                                 update=update_color)

        cls.AlbedoColor = bpy.props.FloatVectorProperty(name="Albedo Color",
                                                        subtype="COLOR",
                                                        size=4,
                                                        min=0,
                                                        max=1,
                                                        update=update_color)
########################################################################################################################
# FLOAT VECTOR PROPERTIES (COORDINATES)
########################################################################################################################
        cls.Location = bpy.props.FloatVectorProperty(name="Location",
                                                     subtype='XYZ',
                                                     update=lambda a, b:
                                                     update_float(a, b, "Location"))

        cls.Rotation = bpy.props.FloatVectorProperty(name="Rotation",
                                                     subtype='EULER',
                                                     update=lambda a, b:
                                                     update_float(a, b, "Rotation"))

        cls.Scale = bpy.props.FloatVectorProperty(name="Scale",
                                                  subtype='XYZ',
                                                  update=lambda a, b:
                                                  update_float(a, b, "Scale"))

        cls.DetailMapLocation = bpy.props.FloatVectorProperty(name="Location",
                                                              subtype='XYZ',
                                                              update=lambda a, b:
                                                              update_float(a, b, "Detail Map Location"))

        cls.DetailMapRotation = bpy.props.FloatVectorProperty(name="Rotation",
                                                              subtype='EULER',
                                                              update=lambda a, b:
                                                              update_float(a, b, "Detail Map Rotation"))

        cls.DetailMapScale = bpy.props.FloatVectorProperty(name="Scale",
                                                           subtype='XYZ',
                                                           update=lambda a, b:
                                                           update_float(a, b, "Detail Map Scale"))
########################################################################################################################
# STRING PROPERTIES
########################################################################################################################
        cls.conf_path = bpy.props.StringProperty(name="Path to textures",
                                                 default="",
                                                 description="Sets the path to texture folder",
                                                 subtype="DIR_PATH",
                                                 update=update_string)

        cls.texture_pattern = bpy.props.StringProperty(name="Keyword",
                                                       default="",
                                                       description="Keyword to find specific texture pack. "
                                                                   "You can use '-' to describe skip keyword",
                                                       update=update_string)
########################################################################################################################
# ENUM PROPERTIES
########################################################################################################################
        cls.AlphaMode = bpy.props.EnumProperty(items=[('STRAIGHT',
                                                       'Straight',
                                                       ''),
                                                      ('CHANNEL_PACKED',
                                                       'Channel Packed',
                                                       '')],
                                               update=update_alpha)
########################################################################################################################
# UV PROPERTIES
########################################################################################################################
        bpy.types.Scene.UVMap = bpy.props.EnumProperty(items=uv_items,
                                                       update=update_uv)
        bpy.types.Scene.test_collection = bpy.props.CollectionProperty(type=UVMapProp)

    @classmethod
    def unregister(cls):
        del bpy.types.Material.props


def register():
    bpy.utils.register_class(MaterialProps)


def unregister():
    bpy.utils.unregister_class(MaterialProps)
