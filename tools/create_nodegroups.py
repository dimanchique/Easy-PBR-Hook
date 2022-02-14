import bpy
from .global_tools import Tools
from .create_nodes import *

__all__ = ['create_normal_map_inverter', 'create_normal_mix']


def create_normal_map_inverter():
    NormalMapInvert = bpy.data.node_groups.new("NormalMapInverter", "ShaderNodeTree")
    NormalMapInvert.name = "NormalMapInverter"
    create_sockets(NormalMapInvert, ("NodeSocketImage", "NM Input"), socket="INPUT")
    create_sockets(NormalMapInvert, ("NodeSocketImage", "NM Output"), socket="OUTPUT")

    nodes_config = Tools.read_json_data('NormalMapInverterNodes')
    links = Tools.read_json_data('NormalMapInverterNodesLinks')

    __create_and_link_nodes_using_config(nodes_config, links, NormalMapInvert)


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

    nodes_config = Tools.read_json_data('NormalMixNodes')
    links = Tools.read_json_data('NormalMixNodesLinks')

    __create_and_link_nodes_using_config(nodes_config, links, NormalMix)


def __create_and_link_nodes_using_config(nodes_config, links, nodetree):
    for node in nodes_config:
        create_node(node_type=nodes_config[node]['node_type'],
                    loc=nodes_config[node]['loc'],
                    node_name=nodes_config[node]['name'],
                    hide=nodes_config[node]['hide'],
                    operation=nodes_config[node]['operation'],
                    blend_type=nodes_config[node]['blend_type'],
                    nodetree=nodetree)
    for link in links:
        link_nodes(links[link]['From'], links[link]['To'], nodetree=nodetree)
