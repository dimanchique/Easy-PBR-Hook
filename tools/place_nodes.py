import bpy
from .create_nodes import *
from ..material_class import Material
from ..properties.material_properties import reset_props, reset_colors
from .update_tool import *

__all__ = ['clear_material', 'place_base', 'place_albedo', 'place_normal_map', 'place_emission',
           'place_specular', 'place_occlusion', 'place_displacement', 'place_opacity', 'place_orm_msk', 'place_orm',
           'place_color_mask', 'place_metal_smoothness', 'place_metal_roughness', 'place_coordinates',
           'place_normal_map_coordinates', 'place_automatic', 'place_manual', 'place_detail_mask', 'remove_detail_mask']


def clear_material():
    nodes = bpy.context.object.active_material.node_tree.nodes
    bpy.context.object.active_material.use_backface_culling = False
    [nodes.remove(nodes[node]) for node in nodes.keys() if node != "Principled BSDF" or node != "Material Output"]
    if "Principled BSDF" not in nodes:
        create_node(node_type="ShaderNodeBsdfPrincipled",
                    loc=(0, 0))
    else:
        nodes["Principled BSDF"].location = (0, 0)
    if "Material Output" not in nodes:
        create_node(node_type="ShaderNodeOutputMaterial",
                    loc=(300, 0))
    else:
        nodes["Material Output"].location = (300, 0)
    link_nodes(FROM("Principled BSDF", "BSDF"),
               TO("Material Output", "Surface"))


def place_base():
    nodes = bpy.context.object.active_material.node_tree.nodes
    clear_material()
    if "Albedo" not in nodes:
        place_albedo()
    if "Normal Map" not in nodes:
        place_normal_map()
    if "Emission" not in nodes:
        place_emission()
    if "Specular" not in nodes:
        place_specular()
    if "Displacement" not in nodes:
        place_displacement()
    if "Opacity" not in nodes:
        place_opacity()


def place_albedo():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Albedo"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, 300),
                    node_name="Albedo",
                    image=current_material.images["Albedo"])
        link_nodes(FROM("Albedo", "Color"),
                   TO("Principled BSDF", "Base Color"))
        if current_material.images["Albedo"].name.lower().split(".")[0].endswith("transparency"):
            link_nodes(FROM("Albedo", "Alpha"),
                       TO("Principled BSDF", "Alpha"))
            current_material.opacity_from_albedo = True
    elif current_material.found_textures["ORM"] or current_material.found_textures["Occlusion"]:
        create_node("ShaderNodeRGB", (-700, 300), node_name="Albedo")
    else:
        return
    Material.add_to_nodes_list("Albedo")


def place_normal_map():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Normal Map"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, -600),
                    node_name="Normal Map",
                    image=current_material.images["Normal Map"])
        create_node(node_type="ShaderNodeNormalMap",
                    loc=(-360, -600),
                    node_name="Normal Map Strength",
                    hide=True)
        if current_material.found_textures["Detail Map"]:
            create_node(node_type="ShaderNodeTexImage",
                        loc=(-700, -900),
                        node_name="Detail Map",
                        image=current_material.images["Detail Map"])
            place_normal_map_coordinates()
            place_normal_mix()
            if current_material.found_textures["Detail Mask"]:
                place_detail_mask()
            link_nodes_in_a_row((FROM("Normal Map", "Color"),
                                 TO("NormalMix", "Main")),
                                (FROM("Detail Map", "Color"),
                                 TO("NormalMix", "Detail")))
            link_nodes_in_a_row((FROM("NormalMix", "Color"),
                                 TO("Normal Map Strength", "Color")),
                                (FROM("Normal Map Strength", "Normal"),
                                 TO("Principled BSDF", "Normal")))
            Material.add_to_nodes_list("Detail Map")
        else:
            link_nodes_in_a_row((FROM("Normal Map", "Color"),
                                 TO("Normal Map Strength", "Color")),
                                (FROM("Normal Map Strength", "Normal"),
                                 TO("Principled BSDF", "Normal")))
        Material.add_to_nodes_list("Normal Map")


def place_detail_mask(new=False):
    current_material = Material.MATERIALS['CURRENT']
    create_node(node_type="ShaderNodeTexImage",
                loc=(-700, -1200),
                node_name="Detail Mask",
                image=current_material.images["Detail Mask"])
    link_nodes_in_a_row((FROM("Detail Mask", "Color"),
                         TO("NormalMix", "Detail Mask")))
    if new:
        if "Mapping" in bpy.context.object.active_material.node_tree.nodes:
            link_nodes(FROM("Mapping", "Vector"),
                       TO("Detail Mask", "Vector"))
    Material.add_to_nodes_list("Detail Mask")


def remove_detail_mask():
    nodes = bpy.context.object.active_material.node_tree.nodes
    nodes.remove(nodes["Detail Mask"])
    Material.remove_from_nodes_list("Detail Mask")


def place_emission():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Emission"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, -300),
                    node_name="Emission",
                    image=current_material.images["Emission"])
        if current_material.simplified_connection:
            link_nodes_in_a_row((FROM("Emission", "Color"),
                                 TO("Principled BSDF", "Emission")))
        else:
            create_node(node_type="ShaderNodeMixRGB",
                        loc=(-360, -300),
                        node_name="Emission Multiply",
                        blend_type="MULTIPLY",
                        default_input=("Fac", 1),
                        hide=True)
            create_node(node_type="ShaderNodeValue",
                        loc=(-360, -350),
                        node_name="Emission Strength",
                        hide=True)
            link_nodes_in_a_row((FROM("Emission", "Color"),
                                 TO("Emission Multiply", "Color1")),
                                (FROM("Emission Strength", "Value"),
                                 TO("Emission Multiply", "Color2")),
                                (FROM("Emission Multiply", "Color"),
                                 TO("Principled BSDF", "Emission")))
        Material.add_to_nodes_list("Emission")


def place_specular():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Specular"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, -1200),
                    node_name="Specular",
                    image=current_material.images["Specular"])
        if current_material.simplified_connection:
            link_nodes_in_a_row((FROM("Specular", "Color"),
                                 TO("Principled BSDF", "Specular")))
        else:
            create_node(node_type="ShaderNodeMath",
                        loc=(-360, -1200),
                        node_name="Specular Add",
                        operation="ADD",
                        hide=True)
            link_nodes_in_a_row((FROM("Specular", "Color"),
                                 TO("Specular Add", "Value")),
                                (FROM("Specular Add", "Value"),
                                 TO("Principled BSDF", "Specular")))
        Material.add_to_nodes_list("Specular")


def place_occlusion():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Occlusion"]:
        nodes = bpy.context.object.active_material.node_tree.nodes
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, 300),
                    node_name="Occlusion",
                    image=current_material.images["Occlusion"])
        create_node(node_type="ShaderNodeMixRGB",
                    loc=(-360, 220),
                    node_name="AO_Mult_Albedo",
                    blend_type="MULTIPLY",
                    default_input=("Fac", 1),
                    hide=True)
        create_node(node_type="ShaderNodeMixRGB",
                    loc=(-360, 170),
                    node_name="AO_Mult_Spec",
                    blend_type="MULTIPLY",
                    default_input=("Fac", 1),
                    hide=True)
        if current_material.found_textures["Specular"]:
            nodes["Specular"].location = (-1000, 0)
            if current_material.simplified_connection:
                link_nodes_in_a_row((FROM("Specular", "Color"),
                                     TO("AO_Mult_Spec", "Color1")))
            else:
                link_nodes_in_a_row((FROM("Specular", "Color"),
                                     TO("Specular Add", "Value")),
                                    (FROM("Specular Add", "Value"),
                                     TO("AO_Mult_Spec", "Color1")))
                nodes["Specular Add"].location = (-360, 50)
        else:
            create_node(node_type="ShaderNodeValue",
                        loc=(-360, 120),
                        node_name="Specular Value",
                        default_output=(0, 0.5),
                        hide=True)
            link_nodes(FROM("Specular Value", "Value"),
                       TO("AO_Mult_Spec", "Color1"))

        link_nodes_in_a_row((FROM("Occlusion", "Color"),
                             TO("AO_Mult_Albedo", "Color2")),
                            (FROM("Occlusion", "Color"),
                             TO("AO_Mult_Spec", "Color2")),
                            (FROM("Albedo", "Color"),
                             TO("AO_Mult_Albedo", "Color1")),
                            (FROM("AO_Mult_Albedo", "Color"),
                             TO("Principled BSDF", "Base Color")),
                            (FROM("AO_Mult_Spec", "Color"),
                             TO("Principled BSDF", "Specular")))
        Material.add_to_nodes_list("Occlusion")


def place_displacement():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Displacement"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, -900),
                    node_name="Displacement",
                    image=current_material.images["Displacement"])
        create_node(node_type="ShaderNodeDisplacement",
                    loc=(-360, -950),
                    node_name="Normal Displacement",
                    hide=True)
        link_nodes_in_a_row((FROM("Displacement", "Color"),
                             TO("Normal Displacement", "Height")),
                            (FROM("Normal Displacement", "Displacement"),
                             TO("Material Output", "Displacement")))
        Material.add_to_nodes_list("Displacement")


def place_opacity():
    current_material = Material.MATERIALS['CURRENT']
    if current_material.found_textures["Opacity"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, -600),
                    node_name="Opacity",
                    image=current_material.images["Opacity"])
        link_nodes(FROM("Opacity", "Color"),
                   TO("Principled BSDF", "Alpha"))
        Material.add_to_nodes_list("Opacity")


def place_orm_msk():
    place_orm()
    place_color_mask()


def place_orm():
    current_material = Material.MATERIALS['CURRENT']
    place_base()
    nodes = bpy.context.object.active_material.node_tree.nodes
    create_node(node_type="ShaderNodeTexImage",
                loc=(-1000, 0),
                node_name="ORM",
                image=current_material.images["ORM"])
    create_node(node_type="ShaderNodeSeparateRGB",
                loc=(-700, 0),
                node_name="SeparateORM",
                hide=True)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(-360, 220),
                node_name="AO_Mult_Albedo",
                blend_type="MULTIPLY",
                default_input=("Fac", 1),
                hide=True)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(-360, 170),
                node_name="AO_Mult_Spec",
                blend_type="MULTIPLY",
                default_input=("Fac", 1),
                hide=True)
    if not current_material.simplified_connection:
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, 0),
                    node_name="Metallic Add",
                    operation="ADD",
                    hide=True)
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, -50),
                    node_name="Roughness Add",
                    operation="ADD",
                    hide=True)
    if "Specular" in nodes:
        nodes["Specular"].location = (-1000, 300)
        if current_material.simplified_connection:
            link_nodes(FROM("Specular", "Color"),
                       TO("AO_Mult_Spec", "Color1"))
        else:
            nodes["Specular Add"].location = (-700, 350)
            link_nodes(FROM("Specular", "Color"),
                       TO("Specular Add", "Value"))
            link_nodes(FROM("Specular Add", "Value"),
                       TO("AO_Mult_Spec", "Color1"))
    else:
        create_node(node_type="ShaderNodeValue",
                    loc=(-360, 120),
                    node_name="Specular Value",
                    default_output=(0, 0.5),
                    hide=True)
        link_nodes(FROM("Specular Value", "Value"),
                   TO("AO_Mult_Spec", "Color1"))
    link_nodes_in_a_row((FROM("ORM", "Color"),
                         TO("SeparateORM", "Image")),
                        (FROM("SeparateORM", "R"),
                         TO("AO_Mult_Spec", "Color2")),
                        (FROM("SeparateORM", "R"),
                         TO("AO_Mult_Albedo", "Color2")),
                        (FROM("Albedo", "Color"),
                         TO("AO_Mult_Albedo", "Color1")),
                        (FROM("AO_Mult_Albedo", "Color"),
                         TO("Principled BSDF", "Base Color")),
                        (FROM("AO_Mult_Spec", "Color"),
                         TO("Principled BSDF", "Specular")))
    if current_material.simplified_connection:
        link_nodes_in_a_row((FROM("SeparateORM", "G"),
                             TO("Principled BSDF", "Roughness")),
                            (FROM("SeparateORM", "B"),
                             TO("Principled BSDF", "Metallic")))
    else:
        link_nodes_in_a_row((FROM("SeparateORM", "G"),
                             TO("Roughness Add", "Value")),
                            (FROM("Roughness Add", "Value"),
                             TO("Principled BSDF", "Roughness")),
                            (FROM("SeparateORM", "B"),
                             TO("Metallic Add", "Value")),
                            (FROM("Metallic Add", "Value"),
                             TO("Principled BSDF", "Metallic")))
    Material.add_to_nodes_list("ORM")


def place_color_mask():
    current_material = Material.MATERIALS['CURRENT']
    nodes = bpy.context.object.active_material.node_tree.nodes
    create_node(node_type="ShaderNodeTexImage",
                loc=(-1300, 300),
                node_name="Color Mask",
                image=current_material.images["Color Mask"])
    create_node(node_type="ShaderNodeSeparateRGB",
                loc=(-1200, 333),
                node_name="SeparateMSK",
                hide=True)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(-970, 570),
                node_name="MixRed",
                blend_type="MULTIPLY",
                hide=True)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(-770, 570),
                node_name="MixGreen",
                blend_type="MULTIPLY",
                hide=True)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(-570, 570),
                node_name="MixBlue",
                blend_type="MULTIPLY",
                hide=True)
    create_node(node_type="ShaderNodeRGB",
                loc=(-1300, 800),
                node_name="RedColor")
    create_node(node_type="ShaderNodeRGB",
                loc=(-1100, 800),
                node_name="GreenColor")
    create_node(node_type="ShaderNodeRGB",
                loc=(-900, 800),
                node_name="BlueColor")
    nodes["Albedo"].location = (-1300, 600)
    if "Specular Add" in nodes:
        nodes["Specular Add"].location = (-700, 300)

    link_nodes_in_a_row((FROM("Albedo", "Color"),
                         TO("MixRed", "Color1")),
                        (FROM("Color Mask", "Color"),
                         TO("SeparateMSK", "Image")),
                        (FROM("SeparateMSK", "R"),
                         TO("MixRed", "Fac")),
                        (FROM("SeparateMSK", "G"),
                         TO("MixGreen", "Fac")),
                        (FROM("SeparateMSK", "B"),
                         TO("MixBlue", "Fac")),
                        (FROM("MixRed", "Color"),
                         TO("MixGreen", "Color1")),
                        (FROM("MixGreen", "Color"),
                         TO("MixBlue", "Color1")),
                        (FROM("RedColor", "Color"),
                         TO("MixRed", "Color2")),
                        (FROM("GreenColor", "Color"),
                         TO("MixGreen", "Color2")),
                        (FROM("BlueColor", "Color"),
                         TO("MixBlue", "Color2")),
                        (FROM("MixBlue", "Color"),
                         TO("AO_Mult_Albedo", "Color1")))
    reset_colors()
    Material.add_to_nodes_list("Color Mask")


def place_metal_smoothness():
    current_material = Material.MATERIALS['CURRENT']
    place_base()
    create_node(node_type="ShaderNodeTexImage",
                loc=(-700, 0),
                node_name="Metal Smoothness",
                image=current_material.images["Metal Smoothness"])
    create_node(node_type="ShaderNodeInvert",
                loc=(-360, -50),
                node_name="Invert",
                hide=True)
    if current_material.simplified_connection:
        link_nodes_in_a_row((FROM("Metal Smoothness", "Alpha"),
                             TO("Invert", "Color")),
                            (FROM("Invert", "Color"),
                             TO("Principled BSDF", "Roughness")),
                            (FROM("Metal Smoothness", "Color"),
                             TO("Principled BSDF", "Metallic")))
    else:
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, 0),
                    node_name="Metallic Add",
                    operation="ADD",
                    hide=True)
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, -100),
                    node_name="Roughness Add",
                    operation="ADD",
                    hide=True)
        link_nodes_in_a_row((FROM("Metal Smoothness", "Alpha"),
                             TO("Invert", "Color")),
                            (FROM("Invert", "Color"),
                             TO("Roughness Add", "Value")),
                            (FROM("Roughness Add", "Value"),
                             TO("Principled BSDF", "Roughness")),
                            (FROM("Metal Smoothness", "Color"),
                             TO("Metallic Add", "Value")),
                            (FROM("Metallic Add", "Value"),
                             TO("Principled BSDF", "Metallic")))
    Material.add_to_nodes_list("Metal Smoothness")


def place_metal_roughness():
    current_material = Material.MATERIALS['CURRENT']
    place_base()
    if current_material.found_textures["Metal"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, 0),
                    node_name="Metal",
                    image=current_material.images["Metal"])
        if current_material.simplified_connection:
            link_nodes_in_a_row((FROM("Metal", "Color"),
                                 TO("Principled BSDF", "Metallic")))
        else:
            create_node(node_type="ShaderNodeMath",
                        loc=(-360, 0),
                        node_name="Metallic Add",
                        operation="ADD",
                        hide=True)
            link_nodes_in_a_row((FROM("Metal", "Color"),
                                 TO("Metallic Add", "Value")),
                                (FROM("Metallic Add", "Value"),
                                 TO("Principled BSDF", "Metallic")))
        Material.add_to_nodes_list("Metal")
    if current_material.found_textures["Roughness"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, -300),
                    node_name="Roughness",
                    image=current_material.images["Roughness"])
        if current_material.simplified_connection:
            link_nodes_in_a_row((FROM("Roughness", "Color"),
                                 TO("Principled BSDF", "Roughness")))
        else:
            create_node(node_type="ShaderNodeMath",
                        loc=(-360, -250),
                        node_name="Roughness Add",
                        operation="ADD",
                        hide=True)
            link_nodes_in_a_row((FROM("Roughness", "Color"),
                                 TO("Roughness Add", "Value")),
                                (FROM("Roughness Add", "Value"),
                                 TO("Principled BSDF", "Roughness")))
        Material.add_to_nodes_list("Roughness")


def place_coordinates():
    current_material = Material.MATERIALS['CURRENT']
    nodes = bpy.context.object.active_material.node_tree.nodes
    uv_layers = bpy.data.meshes[bpy.context.active_object.data.name].uv_layers
    if uv_layers:
        create_node(node_type="ShaderNodeUVMap",
                    loc=(-1900, 600),
                    node_name="UVMap")
        create_node(node_type="ShaderNodeMapping",
                    loc=(-1700, 600),
                    node_name="Mapping")
        nodes['UVMap'].uv_map = uv_layers.keys()[0]
        link_nodes(FROM("UVMap", "UV"),
                   TO("Mapping", "Vector"))
        for texture in current_material.found_textures:
            if current_material.found_textures[texture] and texture in nodes:
                if texture != "Detail Map":
                    link_nodes(FROM("Mapping", "Vector"),
                               TO(texture, "Vector"))


def place_normal_map_coordinates():
    create_node(node_type="ShaderNodeMapping",
                loc=(-1700, -600),
                node_name="Detail Mapping")
    link_nodes(FROM("Detail Mapping", "Vector"),
               TO("Detail Map", "Vector"))


def place_automatic():
    current_material = Material.MATERIALS['CURRENT']
    place_base()
    if current_material.found_textures["ORM"]:
        place_orm_msk() if current_material.found_textures["Color Mask"] else place_orm()
    else:
        if current_material.found_textures["Metal Smoothness"]:
            place_metal_smoothness()
        elif any(texture in current_material.found_textures for texture in ["Metal", "Roughness"]):
            place_metal_roughness()
        place_occlusion()
    if any(current_material.found_textures[texture] for texture in current_material.found_textures):
        place_coordinates()
    reset_props()


def place_manual(pipeline_type):
    current_material = Material.MATERIALS['CURRENT']
    current_material.soft_reset()
    current_material.automatic_mode = False
    if pipeline_type == "MetalRoughness":
        place_metal_roughness()
    elif pipeline_type == "MetalSmoothness":
        place_metal_smoothness()
    elif pipeline_type == "ORM":
        place_orm()
    elif pipeline_type == "ORM+MSK":
        place_orm_msk()
    if not any([pipeline_type == "ORM", pipeline_type == "ORM+MSK"]):
        place_occlusion()
    place_coordinates()
    reset_props()
