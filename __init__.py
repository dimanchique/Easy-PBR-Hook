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
                'uv_env.uv_map_properties',
                'material_env.material_properties',
                'tools.texture_getter',
                'menus.pipeline_menu',
                'menus.db_editor.string_property',
                'menus.db_changer',
                'menus.texture_operators.orm',
                'menus.texture_operators.metal_smoothness',
                'menus.texture_operators.metal_roughness',
                'menus.texture_operators.orm_msk',
                'menus.opacity_modes.fade',
                'menus.opacity_modes.opaque',
                'menus.opacity_modes.cutout',
                'menus.opacity_menu',
                'subpanels.uv_map_panel',
                'subpanels.texture_list_panel',
                'subpanels.texture_mode_panel',
                'subpanels.texture_props_panel',
                'menus.detail_mask_menu',
                'menus.detail_mask_sources.detail_mask',
                'menus.detail_mask_sources.albedo_alpha',
                'menus.detail_mask_sources.none',
                'subpanels.texture_coordinates_panel',
                'subpanels.detail_map_coordinates_panel',
                'subpanels.opacity_panel']

import sys
import importlib

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
