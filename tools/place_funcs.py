import bpy
from .create_nodes import *
from ..material_env.material_class import Material, add_to_nodes_list
from .update_tool import *

__all__ = ['clear_material', 'clear_images', 'place_base', 'place_albedo', 'place_normal_map', 'place_emission',
           'place_specular', 'place_occlusion', 'place_displacement', 'place_opacity', 'place_orm_msk', 'place_orm',
           'place_color_mask', 'place_metal_smoothness', 'place_metal_roughness', 'place_coordinates',
           'place_normal_map_coordinates', 'place_automatic', 'place_manual']


def clear_material():
    nodes = bpy.context.object.active_material.node_tree.nodes
    bpy.context.object.active_material.use_backface_culling = False
    [nodes.remove(nodes[node]) for node in nodes.keys()]
    create_node(node_type="ShaderNodeBsdfPrincipled",
                loc=(0, 0))
    create_node(node_type="ShaderNodeOutputMaterial",
                loc=(300, 0))
    link_nodes(FROM("Principled BSDF", "BSDF"),
               TO("Material Output", "Surface"))


def clear_images():
    if len(bpy.data.materials) <= 2:
        nodes = bpy.context.object.active_material.node_tree.nodes
        for node in nodes.keys():
            if hasattr(nodes[node], "image"):
                if nodes[node].image is not None:
                    bpy.data.images.remove(nodes[node].image)


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
    if Material.MATERIALS['CURRENT'].found["Albedo"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, 300),
                    node_name="Albedo",
                    image=Material.MATERIALS['CURRENT'].images["Albedo"])
        link_nodes(FROM("Albedo", "Color"),
                   TO("Principled BSDF", "Base Color"))
        if Material.MATERIALS['CURRENT'].images["Albedo"].name.lower().split(".")[0].endswith("transparency"):
            link_nodes(FROM("Albedo", "Alpha"),
                       TO("Principled BSDF", "Alpha"))
            Material.MATERIALS['CURRENT'].opacity_from_albedo = True
    elif Material.MATERIALS['CURRENT'].found["ORM"] or Material.MATERIALS['CURRENT'].found["Occlusion"]:
        create_node("ShaderNodeRGB", (-700, 300), node_name="Albedo")
    else:
        return
    add_to_nodes_list("Albedo")


def place_normal_map():
    if Material.MATERIALS['CURRENT'].found["Normal Map"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, -600),
                    node_name="Normal Map",
                    image=Material.MATERIALS['CURRENT'].images["Normal Map"])
        create_node(node_type="ShaderNodeNormalMap",
                    loc=(-360, -600),
                    node_name="Normal Map Strength",
                    hide=True)
        if Material.MATERIALS['CURRENT'].found["Detail Map"]:
            create_node(node_type="ShaderNodeTexImage",
                        loc=(-700, -900),
                        node_name="Detail Map",
                        image=Material.MATERIALS['CURRENT'].images["Detail Map"])
            place_normal_map_coordinates()
            place_normal_mix()
            if Material.MATERIALS['CURRENT'].found["Detail Mask"]:
                create_node(node_type="ShaderNodeTexImage",
                            loc=(-700, -1200),
                            node_name="Detail Mask",
                            image=Material.MATERIALS['CURRENT'].images["Detail Mask"])
                link_nodes_in_a_row((FROM("Detail Mask", "Color"),
                                     TO("NormalMix", "Detail Mask")))
                add_to_nodes_list("Detail Mask")
            link_nodes_in_a_row((FROM("Normal Map", "Color"),
                                 TO("NormalMix", "Main")),
                                (FROM("Detail Map", "Color"),
                                 TO("NormalMix", "Detail")),
                                (FROM("NormalMix", "Color"),
                                 TO("Normal Map Strength", "Color")))
            add_to_nodes_list("Detail Map")
        else:
            link_nodes_in_a_row((FROM("Normal Map", "Color"),
                                 TO("Normal Map Strength", "Color")))
        link_nodes_in_a_row((FROM("Normal Map Strength", "Normal"),
                             TO("Principled BSDF", "Normal")))
        add_to_nodes_list("Normal Map")


def place_emission():
    if Material.MATERIALS['CURRENT'].found["Emission"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, -300),
                    node_name="Emission",
                    image=Material.MATERIALS['CURRENT'].images["Emission"])
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, -300),
                    node_name="Emission Multiply",
                    operation="MULTIPLY", hide=True)
        link_nodes_in_a_row((FROM("Emission", "Color"),
                             TO("Emission Multiply", "Value")),
                            (FROM("Emission Multiply", "Value"),
                             TO("Principled BSDF", "Emission")))
        add_to_nodes_list("Emission")


def place_specular():
    if Material.MATERIALS['CURRENT'].found["Specular"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, -1200),
                    node_name="Specular",
                    image=Material.MATERIALS['CURRENT'].images["Specular"])
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, -1200),
                    node_name="Specular Add",
                    operation="ADD",
                    hide=True)
        link_nodes_in_a_row((FROM("Specular", "Color"),
                             TO("Specular Add", "Value")),
                            (FROM("Specular Add", "Value"),
                             TO("Principled BSDF", "Specular")))
        add_to_nodes_list("Specular")


def place_occlusion():
    if Material.MATERIALS['CURRENT'].found["Occlusion"]:
        nodes = bpy.context.object.active_material.node_tree.nodes
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, 300),
                    node_name="Occlusion",
                    image=Material.MATERIALS['CURRENT'].images["Occlusion"])
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
        if Material.MATERIALS['CURRENT'].found["Specular"]:
            link_nodes_in_a_row((FROM("Specular", "Color"),
                                 TO("Specular Add", "Value")),
                                (FROM("Specular Add", "Value"),
                                 TO("AO_Mult_Spec", "Color1")))
            nodes["Specular Add"].location = (-360, 50)
            nodes["Specular"].location = (-1000, 0)
        else:
            create_node(node_type="ShaderNodeValue",
                        loc=(-360, 120),
                        node_name="Specular Value",
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
        add_to_nodes_list("Occlusion")


def place_displacement():
    if Material.MATERIALS['CURRENT'].found["Displacement"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, -900),
                    node_name="Displacement",
                    image=Material.MATERIALS['CURRENT'].images["Displacement"])
        create_node(node_type="ShaderNodeDisplacement",
                    loc=(-360, -950),
                    node_name="Normal Displacement",
                    hide=True)
        link_nodes_in_a_row((FROM("Displacement", "Color"),
                             TO("Normal Displacement", "Normal")),
                            (FROM("Normal Displacement", "Displacement"),
                             TO("Material Output", "Displacement")))
        add_to_nodes_list("Displacement")


def place_opacity():
    if Material.MATERIALS['CURRENT'].found["Opacity"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, -600),
                    node_name="Opacity",
                    image=Material.MATERIALS['CURRENT'].images["Opacity"])
        link_nodes(FROM("Opacity", "Color"),
                   TO("Principled BSDF", "Alpha"))
        add_to_nodes_list("Opacity")


def place_orm_msk():
    place_orm()
    place_color_mask()


def place_orm():
    place_base()
    create_node(node_type="ShaderNodeTexImage",
                loc=(-1000, 0),
                node_name="ORM",
                image=Material.MATERIALS['CURRENT'].images["ORM"])
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

    if Material.MATERIALS['CURRENT'].found["Specular"]:
        link_nodes(FROM("Specular", "Color"),
                   TO("Specular Add", "Value"))
        link_nodes(FROM("Specular Add", "Value"),
                   TO("AO_Mult_Spec", "Color1"))
        nodes = bpy.context.object.active_material.node_tree.nodes
        nodes["Specular Add"].location = (-700, 350)
        nodes["Specular"].location = (-1000, 300)
    else:
        create_node(node_type="ShaderNodeValue",
                    loc=(-360, 120),
                    node_name="Specular Value",
                    hide=True)
        link_nodes(FROM("Specular Value", "Value"),
                   TO("AO_Mult_Spec", "Color1"))
    link_nodes_in_a_row((FROM("ORM", "Color"),
                         TO("SeparateORM", "Image")),
                        (FROM("SeparateORM", "G"),
                         TO("Roughness Add", "Value")),
                        (FROM("Roughness Add", "Value"),
                         TO("Principled BSDF", "Roughness")),
                        (FROM("SeparateORM", "B"),
                         TO("Metallic Add", "Value")),
                        (FROM("Metallic Add", "Value"),
                         TO("Principled BSDF", "Metallic")),
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
    add_to_nodes_list("ORM")


def place_color_mask():
    nodes = bpy.context.object.active_material.node_tree.nodes
    create_node(node_type="ShaderNodeTexImage",
                loc=(-1300, 300),
                node_name="Color Mask",
                image=Material.MATERIALS['CURRENT'].images["Color Mask"])
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
    if "Specular" in nodes:
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
    add_to_nodes_list("Color Mask")


def place_metal_smoothness():
    place_base()
    create_node(node_type="ShaderNodeTexImage",
                loc=(-700, 0),
                node_name="Metal Smoothness",
                image=Material.MATERIALS['CURRENT'].images["Metal Smoothness"])
    create_node(node_type="ShaderNodeMath",
                loc=(-360, 0),
                node_name="Metallic Add",
                operation="ADD",
                hide=True)
    create_node(node_type="ShaderNodeInvert",
                loc=(-360, -50),
                node_name="Invert",
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
    add_to_nodes_list("Metal Smoothness")


def place_metal_roughness():
    place_base()
    if Material.MATERIALS['CURRENT'].found["Metal"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-700, 0),
                    node_name="Metal",
                    image=Material.MATERIALS['CURRENT'].images["Metal"])
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, 0),
                    node_name="Metallic Add",
                    operation="ADD",
                    hide=True)
        link_nodes_in_a_row((FROM("Metal", "Color"),
                             TO("Metallic Add", "Value")),
                            (FROM("Metallic Add", "Value"),
                             TO("Principled BSDF", "Metallic")))
        add_to_nodes_list("Metal")
    if Material.MATERIALS['CURRENT'].found["Roughness"]:
        create_node(node_type="ShaderNodeTexImage",
                    loc=(-1000, -300),
                    node_name="Roughness",
                    image=Material.MATERIALS['CURRENT'].images["Roughness"])
        create_node(node_type="ShaderNodeMath",
                    loc=(-360, -250),
                    node_name="Roughness Add",
                    operation="ADD",
                    hide=True)
        link_nodes_in_a_row((FROM("Roughness", "Color"),
                             TO("Roughness Add", "Value")),
                            (FROM("Roughness Add", "Value"),
                             TO("Principled BSDF", "Roughness")))
        add_to_nodes_list("Roughness")


def place_coordinates():
    nodes = bpy.context.object.active_material.node_tree.nodes
    create_node(node_type="ShaderNodeUVMap",
                loc=(-1900, 600),
                node_name="UVMap")
    create_node(node_type="ShaderNodeMapping",
                loc=(-1700, 600),
                node_name="Mapping")
    nodes['UVMap'].uv_map = bpy.data.meshes[bpy.context.active_object.data.name].uv_layers.keys()[0]
    link_nodes(FROM("UVMap", "UV"),
               TO("Mapping", "Vector"))
    for texture in Material.MATERIALS['CURRENT'].found:
        if Material.MATERIALS['CURRENT'].found[texture] and texture in nodes:
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
    place_base()
    if Material.MATERIALS['CURRENT'].found["ORM"]:
        place_orm_msk() if Material.MATERIALS['CURRENT'].found["Color Mask"] else place_orm()
    else:
        if Material.MATERIALS['CURRENT'].found["Metal Smoothness"]:
            place_metal_smoothness()
        elif any(texture in Material.MATERIALS['CURRENT'].found for texture in ["Metal", "Roughness"]):
            place_metal_roughness()
        place_occlusion()
    if any(Material.MATERIALS['CURRENT'].found[texture] for texture in Material.MATERIALS['CURRENT'].found):
        place_coordinates()
    reset_props()


def place_manual(pipeline_type):
    Material.MATERIALS['CURRENT'].soft_reset()
    Material.MATERIALS['CURRENT'].automatic = False
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
