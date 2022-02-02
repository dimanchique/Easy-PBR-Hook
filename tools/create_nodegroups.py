import bpy
import json
import os
from .create_nodes import *

__all__ = ['create_normal_map_inverter', 'create_normal_mix']


def create_normal_map_inverter():
    NormalMapInvert = bpy.data.node_groups.new("NormalMapInverter", "ShaderNodeTree")
    NormalMapInvert.name = "NormalMapInverter"
    create_sockets(NormalMapInvert, ("NodeSocketImage", "NM Input"), socket="INPUT")
    create_sockets(NormalMapInvert, ("NodeSocketImage", "NM Output"), socket="OUTPUT")
    nodes_config = load_json_config('NormalMapInverterNodes')
    for node in nodes_config:
        create_node(node_type=nodes_config[node]['node_type'],
                    loc=nodes_config[node]['loc'],
                    node_name=nodes_config[node]['name'],
                    hide=nodes_config[node]['hide'],
                    operation=nodes_config[node]['operation'],
                    blend_type=nodes_config[node]['blend_type'],
                    nodetree=NormalMapInvert)
    links = load_json_config('NormalMapInverterNodesLinks')
    for link in links:
        link_nodes(links[link]['From'], links[link]['To'], nodetree=NormalMapInvert)


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
    nodes_config = load_json_config('NormalMixNodes')
    for node in nodes_config:
        create_node(node_type=nodes_config[node]['node_type'],
                    loc=nodes_config[node]['loc'],
                    node_name=nodes_config[node]['name'],
                    hide=nodes_config[node]['hide'],
                    operation=nodes_config[node]['operation'],
                    blend_type=nodes_config[node]['blend_type'],
                    nodetree=NormalMix)
    links = load_json_config('NormalMixNodesLinks')
    for link in links:
        link_nodes(links[link]['From'], links[link]['To'], nodetree=NormalMix)


def load_json_config(filename):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)+'.json'
    with open(path, 'r') as file:
        return json.load(file)
