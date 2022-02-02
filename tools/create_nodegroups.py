import bpy
from .create_nodes import *

__all__ = ['create_normal_map_inverter', 'create_normal_mix']


def create_normal_map_inverter():
    NormalMapInvert = bpy.data.node_groups.new("NormalMapInverter", "ShaderNodeTree")
    NormalMapInvert.name = "NormalMapInverter"
    create_sockets(NormalMapInvert,
                   ("NodeSocketImage", "NM Input"),
                   socket="INPUT")
    create_sockets(NormalMapInvert,
                   ("NodeSocketImage", "NM Output"),
                   socket="OUTPUT")
    create_node(node_type="NodeGroupInput",
                loc=(-300, 0),
                node_name="Group Input",
                hide=True,
                nodetree=NormalMapInvert)
    create_node(node_type="NodeGroupOutput",
                loc=(340, 0),
                node_name="Group Output",
                hide=True,
                nodetree=NormalMapInvert)
    create_node(node_type="ShaderNodeSeparateRGB",
                loc=(-140, 0),
                node_name="Separate RGB",
                hide=True,
                nodetree=NormalMapInvert)
    create_node(node_type="ShaderNodeCombineRGB",
                loc=(180, 0),
                node_name="Combine RGB",
                hide=True,
                nodetree=NormalMapInvert)
    create_node(node_type="ShaderNodeInvert",
                loc=(20, 0),
                node_name="Invert",
                hide=True,
                nodetree=NormalMapInvert)
    link_nodes_in_a_row((FROM("Group Input", "NM Input"),
                         TO("Separate RGB", "Image")),
                        (FROM("Separate RGB", "R"),
                         TO("Combine RGB", "R")),
                        (FROM("Separate RGB", "B"),
                         TO("Combine RGB", "B")),
                        (FROM("Separate RGB", "G"),
                         TO("Invert", "Color")),
                        (FROM("Invert", "Color"),
                         TO("Combine RGB", "G")),
                        (FROM("Combine RGB", "Image"),
                         TO("Group Output", "NM Output")),
                        nodetree=NormalMapInvert)


def create_normal_mix():
    NormalMix = bpy.data.node_groups.new("NormalMix", "ShaderNodeTree")
    NormalMix.name = "NormalMix"
    create_sockets(NormalMix,
                   ("NodeSocketImage", "Main"),
                   ("NodeSocketImage", "Detail"),
                   ("NodeSocketFloat", "Detail Mask"),
                   socket="INPUT")
    create_sockets(NormalMix,
                   ("NodeSocketImage", "Color"),
                   socket="OUTPUT")
    create_node(node_type="NodeGroupInput",
                loc=(0, -40),
                node_name="Group Input",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="NodeGroupOutput",
                loc=(1400, -36),
                node_name="Group Output",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeSeparateRGB",
                loc=(200, 0),
                node_name="Separate RGB (1)",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeSeparateRGB",
                loc=(200, -75),
                node_name="Separate RGB (2)",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeSeparateRGB",
                loc=(1000, -36),
                node_name="Separate RGB (3)",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeCombineRGB",
                loc=(400, 0),
                node_name="Combine RGB (1)",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeCombineRGB",
                loc=(400, -75),
                node_name="Combine RGB (2)",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeCombineRGB",
                loc=(1200, -36),
                node_name="Combine RGB (3)",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(800, -36),
                node_name="Subtract",
                blend_type="SUBTRACT",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeMixRGB",
                loc=(600, -36),
                node_name="Add",
                blend_type="ADD",
                hide=True,
                nodetree=NormalMix)
    create_node(node_type="ShaderNodeMath",
                loc=(400, -36),
                node_name="Multiply",
                operation="MULTIPLY",
                hide=True,
                nodetree=NormalMix)
    link_nodes_in_a_row((FROM("Group Input", "Main"),
                         TO("Separate RGB (1)", "Image")),
                        (FROM("Group Input", "Detail"),
                         TO("Separate RGB (2)", "Image")),
                        (FROM("Separate RGB (1)", "R"),
                         TO("Combine RGB (1)", "R")),
                        (FROM("Separate RGB (1)", "G"),
                         TO("Combine RGB (1)", "G")),
                        (FROM("Separate RGB (2)", "R"),
                         TO("Combine RGB (2)", "R")),
                        (FROM("Separate RGB (2)", "G"),
                         TO("Combine RGB (2)", "G")),
                        (FROM("Separate RGB (1)", "B"),
                         TO("Multiply", 0)),
                        (FROM("Separate RGB (2)", "B"),
                         TO("Multiply", 1)),
                        (FROM("Combine RGB (1)", "Image"),
                         TO("Add", "Color1")),
                        (FROM("Combine RGB (2)", "Image"),
                         TO("Add", "Color2")),
                        (FROM("Group Input", "Detail Mask"),
                         TO("Add", "Fac")),
                        (FROM("Group Input", "Detail Mask"),
                         TO("Subtract", "Fac")),
                        (FROM("Add", "Color"),
                         TO("Subtract", "Color1")),
                        (FROM("Subtract", "Color"),
                         TO("Separate RGB (3)", "Image")),
                        (FROM("Multiply", "Value"),
                         TO("Combine RGB (3)", "B")),
                        (FROM("Separate RGB (3)", "R"),
                         TO("Combine RGB (3)", "R")),
                        (FROM("Separate RGB (3)", "G"),
                         TO("Combine RGB (3)", "G")),
                        (FROM("Combine RGB (3)", "Image"),
                         TO("Group Output", "Color")),
                        nodetree=NormalMix)
