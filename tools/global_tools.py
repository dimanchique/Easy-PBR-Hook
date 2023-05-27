import bpy
from bpy_extras.io_utils import ExportHelper, ImportHelper
import os
import json

__all__ = ['Tools', 'DataExporter', 'DataImporter', 'RestoreDefaults']


class Tools(bpy.types.PropertyGroup):

    TEXTURES_KEYWORDS_DICT = {}
    TEXTURE_TYPES = []
    TEXTURES_COLORING = {}
    PROP_TO_TEXTURE = {}
    MESSAGES = {}

    @staticmethod
    def validate_path(filename, path):
        if path:
            path = os.path.join(path, filename)
        else:
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename) + '.json'
        return path

    @classmethod
    def read_json_data(cls, filename, path=None):
        path = cls.validate_path(filename, path)
        with open(path, 'r') as file:
            return json.load(file)

    @classmethod
    def write_json_data(cls, data, filename, path=None):
        path = cls.validate_path(filename, path)
        with open(path, 'w') as file:
            json.dump(data, file)

    @classmethod
    def write_textures(cls, path=None):
        cls.write_json_data(cls.TEXTURES_KEYWORDS_DICT, 'texture_mask', path)
        cls.read_textures(path)
        cls.update_panel_masks()

    @classmethod
    def read_textures(cls, path=None):
        cls.TEXTURES_KEYWORDS_DICT = cls.read_json_data('texture_mask', path)
        cls.update_panel_masks()

    @classmethod
    def update_files(cls):
        cls.read_textures()
        cls.TEXTURE_TYPES = list(cls.TEXTURES_KEYWORDS_DICT.keys())
        cls.TEXTURES_COLORING = cls.read_json_data('texture_colors')
        cls.PROP_TO_TEXTURE = cls.read_json_data('prop_to_texture_match')
        cls.MESSAGES = cls.read_json_data('user_messages')

    @classmethod
    def update_panel_masks(cls):
        if hasattr(bpy.context, 'scene') and hasattr(bpy.context.scene, 'db_strings'):
            for texture_name in cls.PROP_TO_TEXTURE:
                setattr(bpy.context.scene.db_strings, texture_name, ', '.join(Tools.TEXTURES_KEYWORDS_DICT[cls.PROP_TO_TEXTURE[texture_name]]))

    @classmethod
    def get_textures_keywords(cls, texture_type):
        return ', '.join(Tools.TEXTURES_KEYWORDS_DICT[texture_type])

    @staticmethod
    def local_update():
        data = dict(bpy.context.scene.db_strings.items())
        for item in data:
            if item in Tools.PROP_TO_TEXTURE:
                texture_string = Tools.TEXTURES_KEYWORDS_DICT[Tools.PROP_TO_TEXTURE[item]]
                line = list(map(str.strip, data[item].lower().split(',')))
                line = [i for i in line if i != '']
                texture_string = []
                texture_string = [i for i in line if i not in texture_string]
                Tools.TEXTURES_KEYWORDS_DICT[Tools.PROP_TO_TEXTURE[item]] = texture_string
        Tools.update_panel_masks()

    @staticmethod
    def global_update():
        Tools.local_update()
        Tools.write_textures()

    @classmethod
    def register(cls):
        cls.update_files()
        cls.write_json_data(cls.TEXTURES_KEYWORDS_DICT, 'default_texture_mask')


class DataExporter(bpy.types.Operator, ExportHelper):
    bl_idname = "pbr.export_data"
    bl_label = "Export User Masks"

    filename_ext = ".json"
    filter_glob = bpy.props.StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        Tools.local_update()
        path, filename = os.path.split(self.filepath)
        Tools.write_json_data(Tools.TEXTURES_KEYWORDS_DICT, filename, path)
        self.report({'INFO'}, Tools.MESSAGES["Database_Export_Success"])
        return {"FINISHED"}


class DataImporter(bpy.types.Operator, ImportHelper):
    bl_idname = "pbr.import_data"
    bl_label = "Import User Masks"

    filename_ext = ".json"
    filter_glob = bpy.props.StringProperty(default="*.json")

    def execute(self, context):
        if DataImporter.filename_ext in self.filepath:
            path, filename = os.path.split(self.filepath)
            Tools.TEXTURES_KEYWORDS_DICT = Tools.read_json_data(filename, path)
            Tools.update_panel_masks()
            self.report({'INFO'}, Tools.MESSAGES["Database_Import_Success"])
        else:
            self.report({'ERROR'}, Tools.MESSAGES["Database_Import_Error"])
        return {"FINISHED"}


class RestoreDefaults(bpy.types.Operator):
    bl_idname = "pbr.restore_defaults"
    bl_label = "Restore Default Masks"

    def execute(self, context):
        Tools.TEXTURES_KEYWORDS_DICT = Tools.read_json_data('default_texture_mask')
        Tools.update_panel_masks()
        self.report({'INFO'}, Tools.MESSAGES["RestoreDefaults"])
        return {"FINISHED"}


def register():
    bpy.utils.register_class(Tools)
    bpy.utils.register_class(DataExporter)
    bpy.utils.register_class(DataImporter)
    bpy.utils.register_class(RestoreDefaults)


def unregister():
    bpy.utils.unregister_class(Tools)
    bpy.utils.unregister_class(DataExporter)
    bpy.utils.unregister_class(DataImporter)
    bpy.utils.unregister_class(RestoreDefaults)
