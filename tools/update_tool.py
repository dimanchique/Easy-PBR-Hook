import bpy
from ..material_class import Material
from .create_nodes import *
from .create_nodegroups import *

__all__ = ['update_float', 'update_normal', 'update_detail', 'update_color', 'update_string',
           'place_normal_map_inverter', 'place_normal_mix', 'remove_normal_map_inverter',
           'update_texture_pattern', 'update_alpha', 'update_uv', 'update_opacity_add']


def update_float(self, context, origin=""):
    nodes = context.object.active_material.node_tree.nodes
    material_prop = context.active_object.active_material.props
    if origin == "Roughness" and "Roughness Add" in nodes:
        nodes["Roughness Add"].inputs[1].default_value = material_prop.RoughnessAdd - 1
    elif origin == "Metallic" and "Metallic Add" in nodes:
        nodes["Metallic Add"].inputs[1].default_value = material_prop.MetallicAdd - 1
    elif origin == "Specular" and "Specular Add" in nodes:
        nodes["Specular Add"].inputs[1].default_value = material_prop.SpecularAdd
    elif origin == "Emission" and "Emission Strength" in nodes:
        nodes["Emission Strength"].outputs[0].default_value = material_prop.EmissionMult
    elif origin == "Normal Strength" and "Normal Map Strength" in nodes:
        nodes["Normal Map Strength"].inputs["Strength"].default_value = material_prop.NormaMapStrength
    elif origin == "AO Strength" and ("AO_Mult_Albedo" in nodes and "AO_Mult_Spec" in nodes):
        nodes["AO_Mult_Albedo"].inputs[0].default_value = nodes["AO_Mult_Spec"].inputs[0].default_value = material_prop.AO_Strength
    elif origin == "Alpha Threshold":
        if context.object.active_material.blend_method != "OPAQUE":
            context.object.active_material.alpha_threshold = material_prop.AlphaThreshold
    elif origin == "Location" and "Mapping" in nodes:
        nodes["Mapping"].inputs["Location"].default_value = material_prop.Location
    elif origin == "Rotation" and "Mapping" in nodes:
        nodes["Mapping"].inputs["Rotation"].default_value = material_prop.Rotation
    elif origin == "Scale" and "Mapping" in nodes:
        nodes["Mapping"].inputs["Scale"].default_value = material_prop.Scale
    elif origin == "Detail Map Location" and "Detail Mapping" in nodes:
        nodes["Detail Mapping"].inputs["Location"].default_value = material_prop.DetailMapLocation
    elif origin == "Detail Map Rotation" and "Detail Mapping" in nodes:
        nodes["Detail Mapping"].inputs["Rotation"].default_value = material_prop.DetailMapRotation
    elif origin == "Detail Map Scale" and "Detail Mapping" in nodes:
        nodes["Detail Mapping"].inputs["Scale"].default_value = material_prop.DetailMapScale
    elif origin == "Detail Mask Strength" and "NormalMix" in nodes:
        nodes["NormalMix"].inputs["Detail Mask"].default_value = material_prop.DetailMaskStrength
    elif origin == "Opacity" and "Opacity Add" in nodes:
        nodes["Opacity Add"].inputs[1].default_value = material_prop.OpacityAdd


def update_normal(self, context):
    material_prop = context.active_object.active_material.props
    if "Normal Map" in Material.MATERIALS['CURRENT'].nodes_list:
        if material_prop.NormalMapInverterEnabled:
            place_normal_map_inverter("Normal")
        else:
            remove_normal_map_inverter("Normal")


def update_detail(self, context):
    material_prop = context.active_object.active_material.props
    if "Detail Map" in Material.MATERIALS['CURRENT'].nodes_list:
        if material_prop.DetailMapInverterEnabled:
            place_normal_map_inverter("Detail")
        else:
            remove_normal_map_inverter("Detail")


def update_color(self, context):
    nodes = context.object.active_material.node_tree.nodes
    material_prop = context.active_object.active_material.props
    if "Albedo" in Material.MATERIALS['CURRENT'].nodes_list and nodes["Albedo"].type == "RGB":
        nodes["Albedo"].outputs["Color"].default_value = material_prop.AlbedoColor
    else:
        nodes["Principled BSDF"].inputs["Base Color"].default_value = material_prop.AlbedoColor
    if "Color Mask" in Material.MATERIALS['CURRENT'].nodes_list:
        nodes["RedColor"].outputs["Color"].default_value = material_prop.MixR
        nodes["GreenColor"].outputs["Color"].default_value = material_prop.MixG
        nodes["BlueColor"].outputs["Color"].default_value = material_prop.MixB


def update_string(self, context):
    material = context.active_object.active_material
    if material.props.textures_path != bpy.path.abspath(material.props.textures_path):
        material.props.textures_path = bpy.path.abspath(material.props.textures_path)
    if Material.MATERIALS['CURRENT'].current_path != material.props.textures_path or \
            Material.MATERIALS['CURRENT'].current_pattern != material.props.textures_pattern:
        Material.MATERIALS['CURRENT'].finished = False


def update_texture_pattern(self, context):
    material = context.active_object.active_material
    if material.props.UseMaterialNameAsKeyword:
        material.props.sub_pattern = material.props.textures_pattern
        material.props.textures_pattern = material.name
        Material.MATERIALS['CURRENT'].texture_pattern = material.name
    else:
        material.props.textures_pattern = material.props.sub_pattern
        Material.MATERIALS['CURRENT'].texture_pattern = material.props.sub_pattern


def update_alpha(self, context):
    material_prop = context.active_object.active_material.props
    bpy.data.images[Material.MATERIALS['CURRENT'].images['Albedo'].name].alpha_mode = material_prop.AlphaMode


def update_uv(self, context):
    nodes = context.object.active_material.node_tree.nodes
    nodes["UVMap"].uv_map = context.scene.UVMap


def place_normal_map_inverter(origin="Normal"):
    nodes = bpy.context.object.active_material.node_tree.nodes
    if "NormalMapInverter" not in bpy.data.node_groups:
        create_normal_map_inverter()
    if origin == "Normal":
        location = (-360, -700)
        node = "Normal Map"
        node_name = "NormalMapInverter"
        socket = "Main"
    else:
        location = (-360, -750)
        node = "Detail Map"
        node_name = "DetailMapInverter"
        socket = "Detail"
    create_node(node_type="ShaderNodeGroup",
                loc=location,
                node_name=node_name,
                nodegroup="NormalMapInverter",
                hide=True)
    if "NormalMix" in nodes:
        link_nodes_in_a_row((FROM(node, "Color"),
                             TO(node_name, "NM Input")),
                            (FROM(node_name, "NM Output"),
                             TO("NormalMix", socket)))
    else:
        link_nodes_in_a_row((FROM("Normal Map", "Color"),
                             TO("NormalMapInverter", "NM Input")),
                            (FROM("NormalMapInverter", "NM Output"),
                             TO("Normal Map Strength", "Color")))


def place_normal_mix():
    if "NormalMix" not in bpy.data.node_groups:
        create_normal_mix()
    create_node(node_type="ShaderNodeGroup",
                loc=(-360, -650),
                node_name="NormalMix",
                nodegroup="NormalMix",
                hide=True)


def remove_normal_map_inverter(origin="Normal"):
    nodes = bpy.context.object.active_material.node_tree.nodes
    if origin == "Normal":
        node = "Normal Map"
        socket = "Main"
        target_node = "NormalMapInverter"
    else:
        node = "Detail Map"
        socket = "Detail"
        target_node = "DetailMapInverter"
    if target_node in nodes:
        nodes.remove(nodes[target_node])
        if "NormalMix" in nodes:
            link_nodes(FROM(node, "Color"), TO("NormalMix", socket))
        else:
            link_nodes(FROM("Normal Map", "Color"), TO("Normal Map Strength", "Color"))


def update_opacity_add(mode):
    nodes = bpy.context.object.active_material.node_tree.nodes
    if mode == 'CLEAR':
        if 'Opacity Add' in nodes:
            from_node_name = nodes['Opacity Add'].inputs['Value'].links[0].from_node.name
            from_socket_name = nodes['Opacity Add'].inputs['Value'].links[0].from_socket.name
            to_node_name = nodes['Opacity Add'].outputs['Value'].links[0].to_node.name
            to_socket_name = nodes['Opacity Add'].outputs['Value'].links[0].to_socket.name
            link_nodes(FROM(from_node_name, from_socket_name), TO(to_node_name, to_socket_name))
            nodes.remove(nodes['Opacity Add'])
        return
    elif mode == 'CREATE':
        location = (0, 0)
        socket_name = ''
        node_name = nodes['Principled BSDF'].inputs['Alpha'].links[0].from_node.name
        if node_name == 'Albedo':
            socket_name = 'Alpha'
            location = (-960, 520) if 'ORM' in Material.MATERIALS['CURRENT'].nodes_list else (-360, 70)
        elif node_name == 'Opacity':
            socket_name = 'Color'
            location = (-700, -560)
        create_node(node_type="ShaderNodeMath",
                    loc=location,
                    node_name="Opacity Add",
                    operation="ADD",
                    default_input=(1, 0),
                    hide=True)
        link_nodes_in_a_row((FROM(node_name, socket_name),
                             TO("Opacity Add", "Value")),
                            (FROM("Opacity Add", "Value"),
                             TO("Principled BSDF", "Alpha")))
    return
