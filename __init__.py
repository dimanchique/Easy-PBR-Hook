import sys
import importlib

bl_info = {
    "name": "Easy PBR Hook",
    "author": "Dmitry F.",
    "version": (1, 5, 2),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Easy PBR Hook",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Material",
}

modulesNames = ['main_panel',                                   # 1. Main Panel
                'panels.texture_mode_panel',                    # 2. Mode Section
                'panels.texture_list_panel',                    # 3. List of founded textures
                'panels.texture_props_panel',                   # 4. Texture Properties
                'panels.texture_coordinates_panel',             # 5. Texture Coordinates Section
                'panels.uv_map_panel',                          # 6. UV Map Choose Sections
                'panels.detail_map_coordinates_panel',          # 7. Detail Map Coordinates Section
                'panels.opacity_panel',                         # 8. Opacity Mode Section
                'properties.uv_map_properties',
                'properties.material_properties',
                'properties.db_properties',
                'menus.pipeline_menu',
                'menus.db_update_menu',
                'menus.opacity_menu',
                'menus.detail_mask_menu',
                'tools.texture_getter']

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
