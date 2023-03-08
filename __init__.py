bl_info = {
    "name": "Easy PBR Hook",
    "author": "Dmitry F.",
    "version": (1, 8, 2),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Easy PBR Hook is an add-on to set up your PBR materials in Blender in 1 click",
    "warning": "",
    "doc_url": "",
    "tracker_url": "https://blendermarket.com/creator/products/easy-pbr-hook",
    "category": "Material",
}

if "bpy" in locals():
    import importlib

    importlib.reload(global_tools)
    importlib.reload(main_panel)
    importlib.reload(texture_mode_panel)
    importlib.reload(texture_list_panel)
    importlib.reload(texture_props_panel)
    importlib.reload(texture_coordinates_panel)
    importlib.reload(uv_map_panel)
    importlib.reload(detail_map_coordinates_panel)
    importlib.reload(opacity_panel)
    importlib.reload(uv_map_properties)
    importlib.reload(db_properties)
    importlib.reload(material_properties)
    importlib.reload(pipeline_menu)
    importlib.reload(db_update_menu)
    importlib.reload(opacity_menu)
    importlib.reload(detail_mask_menu)
    importlib.reload(texture_loader)
    importlib.reload(image_updater)
else:
    from .tools import global_tools
    from . import main_panel
    from .panels import texture_mode_panel
    from .panels import texture_list_panel
    from .panels import texture_props_panel
    from .panels import texture_coordinates_panel
    from .panels import uv_map_panel
    from .panels import detail_map_coordinates_panel
    from .panels import opacity_panel
    from .properties import uv_map_properties
    from .properties import db_properties
    from .properties import material_properties
    from .menus import pipeline_menu
    from .menus import db_update_menu
    from .menus import opacity_menu
    from .menus import detail_mask_menu
    from .tools import texture_loader
    from .tools import image_updater


def register():
    global_tools.register()
    main_panel.register()
    texture_mode_panel.register()
    texture_list_panel.register()
    texture_props_panel.register()
    texture_coordinates_panel.register()
    uv_map_panel.register()
    detail_map_coordinates_panel.register()
    opacity_panel.register()
    uv_map_properties.register()
    db_properties.register()
    material_properties.register()
    pipeline_menu.register()
    db_update_menu.register()
    opacity_menu.register()
    detail_mask_menu.register()
    texture_loader.register()
    image_updater.register()


def unregister():
    image_updater.unregister()
    texture_loader.unregister()
    detail_mask_menu.unregister()
    opacity_menu.unregister()
    db_update_menu.unregister()
    pipeline_menu.unregister()
    material_properties.unregister()
    db_properties.unregister()
    uv_map_properties.unregister()
    opacity_panel.unregister()
    detail_map_coordinates_panel.unregister()
    uv_map_panel.unregister()
    texture_coordinates_panel.unregister()
    texture_props_panel.unregister()
    texture_list_panel.unregister()
    texture_mode_panel.unregister()
    main_panel.unregister()
    global_tools.unregister()


if __name__ == "__main__":
    register()
