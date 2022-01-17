import sys
import importlib

bl_info = {
    "name": "Easy PBR Hook",
    "author": "Dmitry F.",
    "version": (1, 5, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Easy PBR Hook",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Material",
}

modulesNames = ['main_panel',
                'properties.uv_map_properties',
                'properties.material_properties',
                'properties.db_properties',
                'menus.pipeline_menu',
                'menus.db_update_menu',
                'menus.opacity_menu',
                'menus.detail_mask_menu',
                'tools.texture_getter',
                'panels.uv_map_panel',
                'panels.texture_list_panel',
                'panels.texture_mode_panel',
                'panels.texture_props_panel',
                'panels.texture_coordinates_panel',
                'panels.detail_map_coordinates_panel',
                'panels.opacity_panel']

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
