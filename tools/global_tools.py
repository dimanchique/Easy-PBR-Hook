import bpy
from bpy_extras.io_utils import ExportHelper, ImportHelper
import os
import json

__all__ = ['Tools']


class Tools(bpy.types.PropertyGroup):
    ###################################################################################################################
    # TEXTURE MASKS
    ###################################################################################################################
    TEXTURES_MASK = {}
    TEXTURES = []
    TEXTURES_COLORS = {}
    PROP_TO_TEXTURE = {}

    @classmethod
    def update_files(cls):
        cls.read_textures()
        with open(os.path.dirname(os.path.realpath(__file__)) + '\\texture_colors.json', 'r') as file:
            cls.TEXTURES_COLORS = json.load(file)

        with open(os.path.dirname(os.path.realpath(__file__)) + '\\prop_to_texture_match.json', 'r') as file:
            cls.PROP_TO_TEXTURE = json.load(file)

    @staticmethod
    def write_textures(path=None):
        if not path:
            path = os.path.dirname(os.path.realpath(__file__)) + '\\texture_mask.json'
        with open(path, 'w') as file:
            json.dump(Tools.TEXTURES_MASK, file)

    @staticmethod
    def read_textures(path=None):
        if not path:
            path = os.path.dirname(os.path.realpath(__file__)) + '\\texture_mask.json'
        with open(path, 'r') as file:
            Tools.TEXTURES_MASK = json.load(file)
            Tools.TEXTURES = list(Tools.TEXTURES_MASK.keys())
        Tools.write_textures()

        if hasattr(bpy.context, 'scene') and hasattr(bpy.context.scene, 'db_strings'):
            bpy.context.scene.db_strings.albedo = ', '.join(Tools.TEXTURES_MASK['Albedo'])
            bpy.context.scene.db_strings.met_sm = ', '.join(Tools.TEXTURES_MASK['Metal Smoothness'])
            bpy.context.scene.db_strings.metal = ', '.join(Tools.TEXTURES_MASK['Metal'])
            bpy.context.scene.db_strings.rough = ', '.join(Tools.TEXTURES_MASK['Roughness'])
            bpy.context.scene.db_strings.orm = ', '.join(Tools.TEXTURES_MASK['ORM'])
            bpy.context.scene.db_strings.color_mask = ', '.join(Tools.TEXTURES_MASK['Color Mask'])
            bpy.context.scene.db_strings.normal_map = ', '.join(Tools.TEXTURES_MASK['Normal Map'])
            bpy.context.scene.db_strings.emission = ', '.join(Tools.TEXTURES_MASK['Emission'])
            bpy.context.scene.db_strings.specular = ', '.join(Tools.TEXTURES_MASK['Specular'])
            bpy.context.scene.db_strings.occlusion = ', '.join(Tools.TEXTURES_MASK['Occlusion'])
            bpy.context.scene.db_strings.displacement = ', '.join(Tools.TEXTURES_MASK['Displacement'])
            bpy.context.scene.db_strings.opacity = ', '.join(Tools.TEXTURES_MASK['Opacity'])
            bpy.context.scene.db_strings.detail_map = ', '.join(Tools.TEXTURES_MASK['Detail Map'])
            bpy.context.scene.db_strings.detail_mask = ', '.join(Tools.TEXTURES_MASK['Detail Mask'])
    ###################################################################################################################
    # DB UPDATING
    ###################################################################################################################
    @staticmethod
    def local_update():
        data = dict(bpy.context.scene.db_strings.items())
        for item in data:
            if item in Tools.PROP_TO_TEXTURE:
                line = list(map(str.strip, data[item].split(',')))
                line = [i for i in line if i != '']
                Tools.TEXTURES_MASK[Tools.PROP_TO_TEXTURE[item]] = list(set(line))

    @staticmethod
    def global_update():
        Tools.local_update()
        Tools.write_textures()
    ###################################################################################################################
    # MESSAGES
    ###################################################################################################################
    UV_MAP_WARNING_MESSAGE = 'UV Map not found. Please, fix this problem to use Texture coordinates section!'
    TEXTURE_GETTER_WARNING_MESSAGE = 'No textures found! Check path and keyword'
    UPDATE_DATABASE = {'Local': "Database was locally updated!",
                       'Global': "Database was globally updated!"}
    IMAGE_UPDATE = 'Images were updated!'
    DETAIL_MASK_PLACED = 'Detail Mask node was created'
    DETAIL_MASK_REMOVED = 'Detail Mask node was removed'
    SUCCESS_LOADING = 'Textures loaded successfully!'
    EXPORT_FINISHED = 'Masks exported successfully!'
    IMPORT_FINISHED = 'Masks imported successfully!'
    IMPORT_ERROR = 'Unsupported file!'

    @classmethod
    def register(cls):
        cls.update_files()


class DataExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "pbr.export_data"
    bl_label = "Export User Masks"

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob = bpy.props.StringProperty(
            default="*.json",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    def execute(self, context):
        Tools.write_textures(self.filepath)
        self.report({'INFO'}, Tools.EXPORT_FINISHED)
        return {"FINISHED"}


class DataImporter(bpy.types.Operator, ImportHelper):
    bl_idname = "pbr.import_data"
    bl_label = "Import User Masks"

    # ExportHelper mixin class uses this
    filename_ext = ".json"
    filter_glob = bpy.props.StringProperty(default="*.json")

    def execute(self, context):
        if DataImporter.filename_ext in self.filepath:
            Tools.read_textures(self.filepath)
            self.report({'INFO'}, Tools.IMPORT_FINISHED)
        else:
            self.report({'ERROR'}, Tools.IMPORT_ERROR)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(Tools)
    bpy.utils.register_class(DataExporter)
    bpy.utils.register_class(DataImporter)


def unregister():
    bpy.utils.unregister_class(Tools)
    bpy.utils.unregister_class(DataExporter)
    bpy.utils.unregister_class(DataImporter)
