import bpy
import os

####################################################################################################
# CREDITS
####################################################################################################
bl_info = {
    "name": "Easy PBR Hook",
    "author": "Dmitry F.",
    "version": (1, 4, 12),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Easy PBR Hook",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Material",
}


####################################################################################################
# MATERIAL CLASS
####################################################################################################


class Material:
    def __init__(self, name):
        self.name = name
        PBRPanel.MATERIALS[name] = self
        PBRPanel.MATERIALS['CURRENT'] = self
        self.found = dict.fromkeys(TEXTURES, False)
        self.images = dict.fromkeys(TEXTURES, None)
        self.nodeslist = []
        self.opacity_mode = "Opaque"
        self.opacity_from_albedo = False
        self.finished = False
        self.automatic = True
        self.mask_source = "Detail Mask"

    def reset(self):
        self.found = dict.fromkeys(TEXTURES, False)
        self.images = dict.fromkeys(TEXTURES, None)
        self.finished = False
        self.automatic = True
        self.softreset()
        bpy.context.object.active_material.blend_method = "OPAQUE"
        bpy.context.object.active_material.shadow_method = "OPAQUE"

    def softreset(self):
        self.nodeslist = []
        self.opacity_mode = "Opaque"
        self.opacity_from_albedo = False
        self.mask_source = "Detail Mask"


####################################################################################################
# TEXTURES MASK
####################################################################################################


TEXTURES_MASK = {"Albedo": (
    "basecolor", "base_color", "bc", "color", "albedo", "albedotransparency", "albedo_transparency", "diffuse",
    "diffusemap", "diffuse_map", "alb"),
    "Metal Smoothness": (
        "metsm", "met_sm", "metal_smoothness", "metalic_smoothness", "metalsmoothness", "metallicsmoothness",
        "metal_smooth", "metalsmooth", "metsmooth"),
    "Metal": ("met", "metal", "_m", "metall", "metallic"),
    "Roughness": ("_r", "rough", "roughness"),
    "ORM": ("_orm", "occlusionroughnessmetallic"),
    "Color Mask": ("_m", "msk", "colormask", "color_mask", "_mask"),
    "Normal Map": ("normal", "nm", "_n", "normal_map", "normalmap", "normaldx", "normal_dx", "nrm"),
    "Emission": ("_e", "emis", "emiss", "emission"),
    "Specular": ("_s", "specular", "spec"),
    "Occlusion": ("occlusion", "_ao", "ambientocclusion"),
    "Displacement": ("displacement", "height", "hightmap"),
    "Opacity": ("opacity", "transparency"),
    "Detail Map": ("detailnrm", "detail_nrm", "detail", "detailmap", "detail_map", "detail_n", "detailn"),
    "Detail Mask": (
        "detailmsk", "detail_msk", "detailmask", "detail_mask", "detmsk", "det_msk", "detmask",
        "det_mask")}

TEXTURES = list(TEXTURES_MASK.keys())


####################################################################################################
# PROPS CLASS AND ITS UPDATE
####################################################################################################


class MaterialProps(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Material.props = bpy.props.PointerProperty(name="Custom properties",
                                                             description="Custom Properties for Material", type=cls)

        cls.RoughnessAdd = bpy.props.FloatProperty(name="Roughness", min=0, max=1,
                                                   update=lambda a, b: update_float(a, b, "Roughness"))
        cls.MetallicAdd = bpy.props.FloatProperty(name="Metallic", min=0, max=1,
                                                  update=lambda a, b: update_float(a, b, "Metallic"))
        cls.SpecularAdd = bpy.props.FloatProperty(name="Specular", min=0, max=100,
                                                  update=lambda a, b: update_float(a, b, "Specular"))
        cls.EmissionMult = bpy.props.FloatProperty(name="Emission", min=0, max=1,
                                                   update=lambda a, b: update_float(a, b, "Emission"))
        cls.NormaMaplStrength = bpy.props.FloatProperty(name="Normal Strength", min=0,
                                                        update=lambda a, b: update_float(a, b, "Normal Strength"))
        cls.AO_Strength = bpy.props.FloatProperty(name="AO Strength", min=0, max=1,
                                                  update=lambda a, b: update_float(a, b, "AO Strength"))
        cls.AlphaThreshold = bpy.props.FloatProperty(name="Alpha Threshold", min=0, max=1,
                                                     update=lambda a, b: update_float(a, b, "Alpha Threshold"))

        cls.DetailMaskStrength = bpy.props.FloatProperty(name="Detail Mask Strength", min=0, max=1,
                                                         update=lambda a, b: update_float(a, b, "Detail Mask Strength"))

        cls.NormalMapInverterEnabled = bpy.props.BoolProperty(name="Invert Normal", update=update_normal)
        cls.DetailMapInvertorEnabled = bpy.props.BoolProperty(name="Invert Detail", update=update_detail)

        cls.MixR = bpy.props.FloatVectorProperty(name="Red сhannel", subtype="COLOR", size=4, min=0, max=1,
                                                 update=update_color)
        cls.MixG = bpy.props.FloatVectorProperty(name="Green сhannel", subtype="COLOR", size=4, min=0, max=1,
                                                 update=update_color)
        cls.MixB = bpy.props.FloatVectorProperty(name="Blue сhannel", subtype="COLOR", size=4, min=0, max=1,
                                                 update=update_color)
        cls.AlbedoColor = bpy.props.FloatVectorProperty(name="Albedo Color", subtype="COLOR", size=4, min=0, max=1,
                                                        update=update_color)

        cls.conf_path = bpy.props.StringProperty(
            name="Path to textures", default="", description="Sets the path to texture folder",
            subtype="DIR_PATH", update=update_string)
        cls.texture_pattern = bpy.props.StringProperty(
            name="Keyword", default="",
            description="Keyword to find specific texture pack. You can use '-' to describe skip keyword",
            update=update_string)

        cls.Location = bpy.props.FloatVectorProperty(name="Location", subtype='XYZ',
                                                     update=lambda a, b: update_float(a, b, "Location"))
        cls.Rotation = bpy.props.FloatVectorProperty(name="Rotation", subtype='EULER',
                                                     update=lambda a, b: update_float(a, b, "Rotation"))
        cls.Scale = bpy.props.FloatVectorProperty(name="Scale", subtype='XYZ',
                                                  update=lambda a, b: update_float(a, b, "Scale"))

        cls.DetailMapLocation = bpy.props.FloatVectorProperty(name="Location", subtype='XYZ',
                                                              update=lambda a, b: update_float(a, b,
                                                                                               "Detail Map Location"))
        cls.DetailMapRotation = bpy.props.FloatVectorProperty(name="Rotation", subtype='EULER',
                                                              update=lambda a, b: update_float(a, b,
                                                                                               "Detail Map Rotation"))
        cls.DetailMapScale = bpy.props.FloatVectorProperty(name="Scale", subtype='XYZ',
                                                           update=lambda a, b: update_float(a, b, "Detail Map Scale"))

        cls.AlphaMode = bpy.props.EnumProperty(
            items=[('STRAIGHT', 'Straight', ''), ('CHANNEL_PACKED', 'Channel Packed', '')], update=update_alpha)
        cls.OpacityAdd = bpy.props.FloatProperty(name="Opacity", min=0, max=1,
                                                 update=lambda a, b: update_float(a, b, "Opacity"))

        bpy.types.Scene.UVMap = bpy.props.EnumProperty(items=uv_items, update=update_uv)
        bpy.types.Scene.test_collection = bpy.props.CollectionProperty(type=UVMapProp)

    @classmethod
    def unregister(cls):
        del bpy.types.Material.props


def update_float(self, context, origin=""):
    nodes = context.object.active_material.node_tree.nodes
    material_prop = context.active_object.active_material.props
    if origin == "Roughness" and "Roughness Add" in nodes:
        nodes["Roughness Add"].inputs[1].default_value = material_prop.RoughnessAdd - 1
    elif origin == "Metallic" and "Metallic Add" in nodes:
        nodes["Metallic Add"].inputs[1].default_value = material_prop.MetallicAdd - 1
    elif origin == "Specular" and "Specular Add" in nodes:
        nodes["Specular Add"].inputs[1].default_value = material_prop.SpecularAdd
    elif origin == "Emission" and "Emission Multiply" in nodes:
        nodes["Emission Multiply"].inputs[1].default_value = material_prop.EmissionMult
    elif origin == "Normal Strength" and "Normal Map Strength" in nodes:
        nodes["Normal Map Strength"].inputs["Strength"].default_value = material_prop.NormaMaplStrength
    elif origin == "AO Strength" and all(AO in nodes for AO in ["AO_Mult_Albedo", "AO_Mult_Spec"]):
        nodes["AO_Mult_Albedo"].inputs[0].default_value = nodes["AO_Mult_Spec"].inputs[
            0].default_value = material_prop.AO_Strength
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
    if "Normal Map" in PBRPanel.MATERIALS['CURRENT'].nodeslist:
        if material_prop.NormalMapInverterEnabled:
            place_normal_map_invertor("Normal")
        else:
            remove_normal_map_invertor("Normal")


def update_detail(self, context):
    material_prop = context.active_object.active_material.props
    if "Detail Map" in PBRPanel.MATERIALS['CURRENT'].nodeslist:
        if material_prop.DetailMapInvertorEnabled:
            place_normal_map_invertor("Detail")
        else:
            remove_normal_map_invertor("Detail")


def place_normal_map_invertor(origin="Normal"):
    nodes = bpy.context.object.active_material.node_tree.nodes
    if "NormalMapInverter" not in bpy.data.node_groups:
        create_normal_map_inverter()
    if origin == "Normal":
        location = (-360, -700)
        node = "Normal Map"
        nodename = "NormalMapInverter"
        socket = "Main"
    else:
        location = (-360, -750)
        node = "Detail Map"
        nodename = "DetailMapInvertor"
        socket = "Detail"
    create_node("ShaderNodeGroup", location, nodename=nodename, nodegroup="NormalMapInverter", hide=True)
    if "NormalMix" in nodes:
        link_nodes_in_a_row((FROM(node, "Color"), TO(nodename, "NM Input")),
                            (FROM(nodename, "NM Output"), TO("NormalMix", socket)))
    else:
        link_nodes_in_a_row((FROM("Normal Map", "Color"), TO("NormalMapInverter", "NM Input")),
                            (FROM("NormalMapInverter", "NM Output"), TO("Normal Map Strength", "Color")))


def place_normal_mix():
    if "NormalMix" not in bpy.data.node_groups:
        create_normal_mix()
    create_node("ShaderNodeGroup", (-360, -650), nodename="NormalMix", nodegroup="NormalMix", hide=True)


def remove_normal_map_invertor(origin="Normal"):
    nodes = bpy.context.object.active_material.node_tree.nodes
    if origin == "Normal":
        node = "Normal Map"
        socket = "Main"
        target_node = "NormalMapInverter"
    else:
        node = "Detail Map"
        socket = "Detail"
        target_node = "DetailMapInvertor"
    if target_node in nodes:
        nodes.remove(nodes[target_node])
        if "NormalMix" in nodes:
            link_nodes(FROM(node, "Color"), TO("NormalMix", socket))
        else:
            link_nodes(FROM("Normal Map", "Color"), TO("Normal Map Strength", "Color"))


def update_color(self, context):
    nodes = context.object.active_material.node_tree.nodes
    material_prop = context.active_object.active_material.props
    if "Albedo" in PBRPanel.MATERIALS['CURRENT'].nodeslist and nodes["Albedo"].type == "RGB":
        nodes["Albedo"].outputs["Color"].default_value = material_prop.AlbedoColor
    else:
        nodes["Principled BSDF"].inputs["Base Color"].default_value = material_prop.AlbedoColor
    if "Color Mask" in PBRPanel.MATERIALS['CURRENT'].nodeslist:
        nodes["RedColor"].outputs["Color"].default_value = material_prop.MixR
        nodes["GreenColor"].outputs["Color"].default_value = material_prop.MixG
        nodes["BlueColor"].outputs["Color"].default_value = material_prop.MixB


def update_string(self, context):
    if context.active_object.active_material.props.conf_path != bpy.path.abspath(context.active_object.active_material.props.conf_path):
        context.active_object.active_material.props.conf_path = bpy.path.abspath(context.active_object.active_material.props.conf_path)
    if PBRPanel.current_path != context.active_object.active_material.props.conf_path or PBRPanel.current_pattern != context.active_object.active_material.props.texture_pattern:
        PBRPanel.MATERIALS['CURRENT'].finished = False


def update_alpha(self, context):
    material_prop = context.active_object.active_material.props
    bpy.data.images[PBRPanel.MATERIALS['CURRENT'].images['Albedo'].name].alpha_mode = material_prop.AlphaMode


def update_uv(self, context):
    nodes = context.object.active_material.node_tree.nodes
    nodes["UVMap"].uv_map = context.scene.UVMap


def reset_props():
    prop = bpy.context.active_object.active_material.props
    prop.RoughnessAdd = 1
    prop.MetallicAdd = 1
    prop.SpecularAdd = 1
    prop.EmissionMult = 1
    prop.NormaMaplStrength = 1
    prop.AO_Strength = 1
    prop.AlphaThreshold = 0
    prop.NormalMapInverterEnabled = False
    prop.DetailMapInvertorEnabled = False
    prop.MixR = (1, 1, 1, 1)
    prop.MixG = (1, 1, 1, 1)
    prop.MixB = (1, 1, 1, 1)
    prop.Location = (0, 0, 0)
    prop.Rotation = (0, 0, 0)
    prop.Scale = (1, 1, 1)
    prop.DetailMapLocation = (0, 0, 0)
    prop.DetailMapRotation = (0, 0, 0)
    prop.DetailMapScale = (1, 1, 1)
    prop.OpacityAdd = 0


def reset_colors():
    nodes = bpy.context.object.active_material.node_tree.nodes
    nodes["RedColor"].outputs["Color"].default_value = (1, 1, 1, 1)
    nodes["GreenColor"].outputs["Color"].default_value = (1, 1, 1, 1)
    nodes["BlueColor"].outputs["Color"].default_value = (1, 1, 1, 1)


class UVMapProp(bpy.types.PropertyGroup):
    uv: bpy.props.StringProperty()


def uv_items(self, context):
    enum_items = []
    for UV in bpy.data.meshes[context.active_object.data.name].uv_layers.keys():
        data = str(UV)
        item = (data, data, '')
        enum_items.append(item)
    return enum_items


####################################################################################################
# NODE FUNCTIONS
####################################################################################################
def create_node(nodetype, location, nodename="", blendtype="", operation="", nodegroup=None, image=None, hide=False, defaultinput=None, nodetree="default"):
    nodes = bpy.context.object.active_material.node_tree.nodes if nodetree == "default" else nodetree.nodes
    newnode = nodes.new(nodetype)
    newnode.location = location
    if nodename:
        newnode.label = newnode.name = nodename
    if blendtype:
        newnode.blend_type = blendtype
    if operation:
        newnode.operation = operation
    if nodegroup:
        newnode.node_tree = bpy.data.node_groups[nodegroup]
    if image:
        newnode.image = image
    if defaultinput:
        newnode.inputs[defaultinput[0]].default_value = defaultinput[1]
    newnode.hide = hide


def link_nodes(FROM, TO, nodetree="default"):
    node_tree = bpy.context.object.active_material.node_tree if nodetree == "default" else nodetree
    node_tree.links.new(node_tree.nodes[FROM[0]].outputs[FROM[1]], node_tree.nodes[TO[0]].inputs[TO[1]])


def link_nodes_in_a_row(*routes, nodetree="default"):
    [link_nodes((route[0][0], route[0][1]), (route[1][0], route[1][1]), nodetree) for route in routes]


def FROM(name, socket):
    return [name, socket]


def TO(name, socket):
    return [name, socket]


def create_sockets(node, *sockets, socket=""):
    node_sockets = node.inputs if socket == "INPUT" else node.outputs
    [node_sockets.new(sockettype, socket) for sockettype, socket in sockets]


####################################################################################################
# CREATING NODE GROUPS
####################################################################################################
def create_normal_map_inverter():
    NormalMapInvert = bpy.data.node_groups.new("NormalMapInverter", "ShaderNodeTree")
    NormalMapInvert.name = "NormalMapInverter"
    create_sockets(NormalMapInvert, ("NodeSocketImage", "NM Input"), socket="INPUT")
    create_sockets(NormalMapInvert, ("NodeSocketImage", "NM Output"), socket="OUTPUT")
    create_node("NodeGroupInput", (-300, 0), nodename="Group Input", hide=True, nodetree=NormalMapInvert)
    create_node("NodeGroupOutput", (340, 0), nodename="Group Output", hide=True, nodetree=NormalMapInvert)
    create_node("ShaderNodeSeparateRGB", (-140, 0), nodename="Separate RGB", hide=True, nodetree=NormalMapInvert)
    create_node("ShaderNodeCombineRGB", (180, 0), nodename="Combine RGB", hide=True, nodetree=NormalMapInvert)
    create_node("ShaderNodeInvert", (20, 0), nodename="Invert", hide=True, nodetree=NormalMapInvert)
    link_nodes_in_a_row((FROM("Group Input", "NM Input"), TO("Separate RGB", "Image")),
                        (FROM("Separate RGB", "R"), TO("Combine RGB", "R")),
                        (FROM("Separate RGB", "B"), TO("Combine RGB", "B")),
                        (FROM("Separate RGB", "G"), TO("Invert", "Color")),
                        (FROM("Invert", "Color"), TO("Combine RGB", "G")),
                        (FROM("Combine RGB", "Image"), TO("Group Output", "NM Output")), nodetree=NormalMapInvert)


def create_normal_mix():
    NormalMix = bpy.data.node_groups.new("NormalMix", "ShaderNodeTree")
    NormalMix.name = "NormalMix"
    create_sockets(NormalMix, ("NodeSocketImage", "Main"), ("NodeSocketImage", "Detail"),
                   ("NodeSocketFloat", "Detail Mask"), socket="INPUT")
    create_sockets(NormalMix, ("NodeSocketImage", "Color"), socket="OUTPUT")
    create_node("NodeGroupInput", (0, -40), nodename="Group Input", hide=True, nodetree=NormalMix)
    create_node("NodeGroupOutput", (1400, -36), nodename="Group Output", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeSeparateRGB", (200, 0), nodename="Separate RGB (1)", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeSeparateRGB", (200, -75), nodename="Separate RGB (2)", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeSeparateRGB", (1000, -36), nodename="Separate RGB (3)", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeCombineRGB", (400, 0), nodename="Combine RGB (1)", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeCombineRGB", (400, -75), nodename="Combine RGB (2)", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeCombineRGB", (1200, -36), nodename="Combine RGB (3)", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeMixRGB", (800, -36), nodename="Subtract", blendtype="SUBTRACT", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeMixRGB", (600, -36), nodename="Add", blendtype="ADD", hide=True, nodetree=NormalMix)
    create_node("ShaderNodeMath", (400, -36), nodename="Multiply", operation="MULTIPLY", hide=True, nodetree=NormalMix)
    link_nodes_in_a_row((FROM("Group Input", "Main"), TO("Separate RGB (1)", "Image")),
                        (FROM("Group Input", "Detail"), TO("Separate RGB (2)", "Image")),
                        (FROM("Separate RGB (1)", "R"), TO("Combine RGB (1)", "R")),
                        (FROM("Separate RGB (1)", "G"), TO("Combine RGB (1)", "G")),
                        (FROM("Separate RGB (2)", "R"), TO("Combine RGB (2)", "R")),
                        (FROM("Separate RGB (2)", "G"), TO("Combine RGB (2)", "G")),
                        (FROM("Separate RGB (1)", "B"), TO("Multiply", 0)),
                        (FROM("Separate RGB (2)", "B"), TO("Multiply", 1)),
                        (FROM("Combine RGB (1)", "Image"), TO("Add", "Color1")),
                        (FROM("Combine RGB (2)", "Image"), TO("Add", "Color2")),
                        (FROM("Group Input", "Detail Mask"), TO("Add", "Fac")),
                        (FROM("Group Input", "Detail Mask"), TO("Subtract", "Fac")),
                        (FROM("Add", "Color"), TO("Subtract", "Color1")),
                        (FROM("Subtract", "Color"), TO("Separate RGB (3)", "Image")),
                        (FROM("Multiply", "Value"), TO("Combine RGB (3)", "B")),
                        (FROM("Separate RGB (3)", "R"), TO("Combine RGB (3)", "R")),
                        (FROM("Separate RGB (3)", "G"), TO("Combine RGB (3)", "G")),
                        (FROM("Combine RGB (3)", "Image"), TO("Group Output", "Color")), nodetree=NormalMix)


####################################################################################################
# PLACE FUNCTIONS
####################################################################################################
def clear_material():
    nodes = bpy.context.object.active_material.node_tree.nodes
    bpy.context.object.active_material.use_backface_culling = False
    [nodes.remove(nodes[node]) for node in nodes.keys()]
    create_node("ShaderNodeBsdfPrincipled", (0, 0))
    create_node("ShaderNodeOutputMaterial", (300, 0))
    link_nodes(FROM("Principled BSDF", "BSDF"), TO("Material Output", "Surface"))


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
    if PBRPanel.MATERIALS['CURRENT'].found["Albedo"]:
        create_node("ShaderNodeTexImage", (-700, 300), nodename="Albedo",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Albedo"])
        link_nodes(FROM("Albedo", "Color"), TO("Principled BSDF", "Base Color"))
        if PBRPanel.MATERIALS['CURRENT'].images["Albedo"].name.lower().split(".")[0].endswith("transparency"):
            link_nodes(FROM("Albedo", "Alpha"), TO("Principled BSDF", "Alpha"))
            PBRPanel.MATERIALS['CURRENT'].opacity_from_albedo = True
    elif PBRPanel.MATERIALS['CURRENT'].found["ORM"] or PBRPanel.MATERIALS['CURRENT'].found["Occlusion"]:
        create_node("ShaderNodeRGB", (-700, 300), nodename="Albedo")
    else:
        return
    check_and_add_to_nodeslist("Albedo")


def place_normal_map():
    if PBRPanel.MATERIALS['CURRENT'].found["Normal Map"]:
        create_node("ShaderNodeTexImage", (-700, -600), nodename="Normal Map",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Normal Map"])
        create_node("ShaderNodeNormalMap", (-360, -600), nodename="Normal Map Strength", hide=True)
        if PBRPanel.MATERIALS['CURRENT'].found["Detail Map"]:
            create_node("ShaderNodeTexImage", (-700, -900), nodename="Detail Map",
                        image=PBRPanel.MATERIALS['CURRENT'].images["Detail Map"])
            place_normal_map_coordinates()
            place_normal_mix()
            if PBRPanel.MATERIALS['CURRENT'].found["Detail Mask"]:
                create_node("ShaderNodeTexImage", (-700, -1200), nodename="Detail Mask",
                            image=PBRPanel.MATERIALS['CURRENT'].images["Detail Mask"])
                link_nodes_in_a_row((FROM("Detail Mask", "Color"), TO("NormalMix", "Detail Mask")))
                check_and_add_to_nodeslist("Detail Mask")
            link_nodes_in_a_row((FROM("Normal Map", "Color"), TO("NormalMix", "Main")),
                                (FROM("Detail Map", "Color"), TO("NormalMix", "Detail")),
                                (FROM("NormalMix", "Color"), TO("Normal Map Strength", "Color")))
            check_and_add_to_nodeslist("Detail Map")
        else:
            link_nodes_in_a_row((FROM("Normal Map", "Color"), TO("Normal Map Strength", "Color")))
        link_nodes_in_a_row((FROM("Normal Map Strength", "Normal"), TO("Principled BSDF", "Normal")))
        check_and_add_to_nodeslist("Normal Map")


def place_emission():
    if PBRPanel.MATERIALS['CURRENT'].found["Emission"]:
        create_node("ShaderNodeTexImage", (-700, -300), nodename="Emission",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Emission"])
        create_node("ShaderNodeMath", (-360, -300), nodename="Emission Multiply", operation="MULTIPLY", hide=True)
        link_nodes_in_a_row((FROM("Emission", "Color"), TO("Emission Multiply", "Value")),
                            (FROM("Emission Multiply", "Value"), TO("Principled BSDF", "Emission")))
        check_and_add_to_nodeslist("Emission")


def place_specular():
    if PBRPanel.MATERIALS['CURRENT'].found["Specular"]:
        create_node("ShaderNodeTexImage", (-700, -1200), nodename="Specular",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Specular"])
        create_node("ShaderNodeMath", (-360, -1200), nodename="Specular Add", operation="ADD", hide=True)
        link_nodes_in_a_row((FROM("Specular", "Color"), TO("Specular Add", "Value")),
                            (FROM("Specular Add", "Value"), TO("Principled BSDF", "Specular")))
        check_and_add_to_nodeslist("Specular")


def place_occlusion():
    if PBRPanel.MATERIALS['CURRENT'].found["Occlusion"]:
        nodes = bpy.context.object.active_material.node_tree.nodes
        create_node("ShaderNodeTexImage", (-1000, 300), nodename="Occlusion",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Occlusion"])
        create_node("ShaderNodeMixRGB", (-360, 220), nodename="AO_Mult_Albedo", blendtype="MULTIPLY",
                    defaultinput=("Fac", 1), hide=True)
        create_node("ShaderNodeMixRGB", (-360, 170), nodename="AO_Mult_Spec", blendtype="MULTIPLY",
                    defaultinput=("Fac", 1), hide=True)
        if PBRPanel.MATERIALS['CURRENT'].found["Specular"]:
            link_nodes_in_a_row((FROM("Specular", "Color"), TO("Specular Add", "Value")),
                                (FROM("Specular Add", "Value"), TO("AO_Mult_Spec", "Color1")))
            nodes["Specular Add"].location = (-360, 50)
            nodes["Specular"].location = (-1000, 0)
        else:
            create_node("ShaderNodeValue", (-360, 120), nodename="Specular Value", hide=True)
            link_nodes(FROM("Specular Value", "Value"), TO("AO_Mult_Spec", "Color1"))

        link_nodes_in_a_row((FROM("Occlusion", "Color"), TO("AO_Mult_Albedo", "Color2")),
                            (FROM("Occlusion", "Color"), TO("AO_Mult_Spec", "Color2")),
                            (FROM("Albedo", "Color"), TO("AO_Mult_Albedo", "Color1")),
                            (FROM("AO_Mult_Albedo", "Color"), TO("Principled BSDF", "Base Color")),
                            (FROM("AO_Mult_Spec", "Color"), TO("Principled BSDF", "Specular")))
        check_and_add_to_nodeslist("Occlusion")


def place_displacement():
    if PBRPanel.MATERIALS['CURRENT'].found["Displacement"]:
        create_node("ShaderNodeTexImage", (-1000, -900), nodename="Displacement",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Displacement"])
        create_node("ShaderNodeDisplacement", (-360, -950), nodename="Normal Displacement", hide=True)
        link_nodes_in_a_row((FROM("Displacement", "Color"), TO("Normal Displacement", "Normal")),
                            (FROM("Normal Displacement", "Displacement"), TO("Material Output", "Displacement")))
        check_and_add_to_nodeslist("Displacement")


def place_opacity():
    if PBRPanel.MATERIALS['CURRENT'].found["Opacity"]:
        create_node("ShaderNodeTexImage", (-1000, -600), nodename="Opacity",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Opacity"])
        link_nodes(FROM("Opacity", "Color"), TO("Principled BSDF", "Alpha"))
        check_and_add_to_nodeslist("Opacity")


def place_orm_msk():
    place_orm()
    place_color_mask()


def place_orm():
    place_base()
    create_node("ShaderNodeTexImage", (-1000, 0), nodename="ORM", image=PBRPanel.MATERIALS['CURRENT'].images["ORM"])
    create_node("ShaderNodeSeparateRGB", (-700, 0), nodename="SeparateORM", hide=True)
    create_node("ShaderNodeMixRGB", (-360, 220), nodename="AO_Mult_Albedo", blendtype="MULTIPLY",
                defaultinput=("Fac", 1), hide=True)
    create_node("ShaderNodeMixRGB", (-360, 170), nodename="AO_Mult_Spec", blendtype="MULTIPLY", defaultinput=("Fac", 1),
                hide=True)
    create_node("ShaderNodeMath", (-360, 0), nodename="Metallic Add", operation="ADD", hide=True)
    create_node("ShaderNodeMath", (-360, -50), nodename="Roughness Add", operation="ADD", hide=True)

    if PBRPanel.MATERIALS['CURRENT'].found["Specular"]:
        link_nodes(FROM("Specular", "Color"), TO("Specular Add", "Value"))
        link_nodes(FROM("Specular Add", "Value"), TO("AO_Mult_Spec", "Color1"))
        nodes = bpy.context.object.active_material.node_tree.nodes
        nodes["Specular Add"].location = (-700, 350)
        nodes["Specular"].location = (-1000, 300)
    else:
        create_node("ShaderNodeValue", (-360, 120), nodename="Specular Value", hide=True)
        link_nodes(FROM("Specular Value", "Value"), TO("AO_Mult_Spec", "Color1"))
    link_nodes_in_a_row((FROM("ORM", "Color"), TO("SeparateORM", "Image")),
                        (FROM("SeparateORM", "G"), TO("Roughness Add", "Value")),
                        (FROM("Roughness Add", "Value"), TO("Principled BSDF", "Roughness")),
                        (FROM("SeparateORM", "B"), TO("Metallic Add", "Value")),
                        (FROM("Metallic Add", "Value"), TO("Principled BSDF", "Metallic")),
                        (FROM("SeparateORM", "R"), TO("AO_Mult_Spec", "Color2")),
                        (FROM("SeparateORM", "R"), TO("AO_Mult_Albedo", "Color2")),
                        (FROM("Albedo", "Color"), TO("AO_Mult_Albedo", "Color1")),
                        (FROM("AO_Mult_Albedo", "Color"), TO("Principled BSDF", "Base Color")),
                        (FROM("AO_Mult_Spec", "Color"), TO("Principled BSDF", "Specular")))
    check_and_add_to_nodeslist("ORM")


def place_color_mask():
    nodes = bpy.context.object.active_material.node_tree.nodes
    create_node("ShaderNodeTexImage", (-1300, 300), nodename="Color Mask",
                image=PBRPanel.MATERIALS['CURRENT'].images["Color Mask"])
    create_node("ShaderNodeSeparateRGB", (-1200, 333), nodename="SeparateMSK", hide=True)
    create_node("ShaderNodeMixRGB", (-970, 570), nodename="MixRed", blendtype="MULTIPLY", hide=True)
    create_node("ShaderNodeMixRGB", (-770, 570), nodename="MixGreen", blendtype="MULTIPLY", hide=True)
    create_node("ShaderNodeMixRGB", (-570, 570), nodename="MixBlue", blendtype="MULTIPLY", hide=True)
    create_node("ShaderNodeRGB", (-1300, 800), nodename="RedColor")
    create_node("ShaderNodeRGB", (-1100, 800), nodename="GreenColor")
    create_node("ShaderNodeRGB", (-900, 800), nodename="BlueColor")
    nodes["Albedo"].location = (-1300, 600)
    if "Specular" in nodes:
        nodes["Specular Add"].location = (-700, 300)

    link_nodes_in_a_row((FROM("Albedo", "Color"), TO("MixRed", "Color1")),
                        (FROM("Color Mask", "Color"), TO("SeparateMSK", "Image")),
                        (FROM("SeparateMSK", "R"), TO("MixRed", "Fac")), (FROM("SeparateMSK", "G"), TO("MixGreen", "Fac")),
                        (FROM("SeparateMSK", "B"), TO("MixBlue", "Fac")),
                        (FROM("MixRed", "Color"), TO("MixGreen", "Color1")),
                        (FROM("MixGreen", "Color"), TO("MixBlue", "Color1")),
                        (FROM("RedColor", "Color"), TO("MixRed", "Color2")),
                        (FROM("GreenColor", "Color"), TO("MixGreen", "Color2")),
                        (FROM("BlueColor", "Color"), TO("MixBlue", "Color2")),
                        (FROM("MixBlue", "Color"), TO("AO_Mult_Albedo", "Color1")))
    reset_colors()
    check_and_add_to_nodeslist("Color Mask")


def place_metal_smoothness():
    place_base()
    create_node("ShaderNodeTexImage", (-700, 0), nodename="Metal Smoothness",
                image=PBRPanel.MATERIALS['CURRENT'].images["Metal Smoothness"])
    create_node("ShaderNodeMath", (-360, 0), nodename="Metallic Add", operation="ADD", hide=True)
    create_node("ShaderNodeInvert", (-360, -50), nodename="Invert", hide=True)
    create_node("ShaderNodeMath", (-360, -100), nodename="Roughness Add", operation="ADD", hide=True)
    link_nodes_in_a_row((FROM("Metal Smoothness", "Alpha"), TO("Invert", "Color")),
                        (FROM("Invert", "Color"), TO("Roughness Add", "Value")),
                        (FROM("Roughness Add", "Value"), TO("Principled BSDF", "Roughness")),
                        (FROM("Metal Smoothness", "Color"), TO("Metallic Add", "Value")),
                        (FROM("Metallic Add", "Value"), TO("Principled BSDF", "Metallic")))
    check_and_add_to_nodeslist("Metal Smoothness")


def place_metal_roughness():
    place_base()
    if PBRPanel.MATERIALS['CURRENT'].found["Metal"]:
        create_node("ShaderNodeTexImage", (-700, 0), nodename="Metal",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Metal"])
        create_node("ShaderNodeMath", (-360, 0), nodename="Metallic Add", operation="ADD", hide=True)
        link_nodes_in_a_row((FROM("Metal", "Color"), TO("Metallic Add", "Value")),
                            (FROM("Metallic Add", "Value"), TO("Principled BSDF", "Metallic")))
        check_and_add_to_nodeslist("Metal")
    if PBRPanel.MATERIALS['CURRENT'].found["Roughness"]:
        create_node("ShaderNodeTexImage", (-1000, -300), nodename="Roughness",
                    image=PBRPanel.MATERIALS['CURRENT'].images["Roughness"])
        create_node("ShaderNodeMath", (-360, -250), nodename="Roughness Add", operation="ADD", hide=True)
        link_nodes_in_a_row((FROM("Roughness", "Color"), TO("Roughness Add", "Value")),
                            (FROM("Roughness Add", "Value"), TO("Principled BSDF", "Roughness")))
        check_and_add_to_nodeslist("Roughness")


def place_coordinates():
    nodes = bpy.context.object.active_material.node_tree.nodes
    create_node("ShaderNodeUVMap", (-1900, 600), nodename="UVMap")
    create_node("ShaderNodeMapping", (-1700, 600), nodename="Mapping")
    nodes['UVMap'].uv_map = bpy.data.meshes[bpy.context.active_object.data.name].uv_layers.keys()[0]
    link_nodes(FROM("UVMap", "UV"), TO("Mapping", "Vector"))
    for texture in PBRPanel.MATERIALS['CURRENT'].found:
        if PBRPanel.MATERIALS['CURRENT'].found[texture] and texture in nodes:
            if texture != "Detail Map":
                link_nodes(FROM("Mapping", "Vector"), TO(texture, "Vector"))


def place_normal_map_coordinates():
    create_node("ShaderNodeMapping", (-1700, -600), nodename="Detail Mapping")
    link_nodes(FROM("Detail Mapping", "Vector"), TO("Detail Map", "Vector"))


def place_automatic():
    place_base()
    if PBRPanel.MATERIALS['CURRENT'].found["ORM"]:
        place_orm_msk() if PBRPanel.MATERIALS['CURRENT'].found["Color Mask"] else place_orm()
    else:
        if PBRPanel.MATERIALS['CURRENT'].found["Metal Smoothness"]:
            place_metal_smoothness()
        elif any(texture in PBRPanel.MATERIALS['CURRENT'].found for texture in ["Metal", "Roughness"]):
            place_metal_roughness()
        place_occlusion()
    if any(PBRPanel.MATERIALS['CURRENT'].found[texture] for texture in PBRPanel.MATERIALS['CURRENT'].found):
        place_coordinates()
    reset_props()


def place_manual(pipeline_type):
    PBRPanel.MATERIALS['CURRENT'].softreset()
    PBRPanel.MATERIALS['CURRENT'].automatic = False
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


####################################################################################################
# SOME ADDITIONAL FUNCTIONS
####################################################################################################
def get_mode():
    return f"Mode: {' + '.join(PBRPanel.MATERIALS['CURRENT'].nodeslist)} ({'Automatic' if PBRPanel.MATERIALS['CURRENT'].automatic else 'Manual'})"


def check_and_add_to_nodeslist(mode):
    if mode not in PBRPanel.MATERIALS['CURRENT'].nodeslist:
        PBRPanel.MATERIALS['CURRENT'].nodeslist.append(mode)


####################################################################################################
# CHANGE OPACITY CLASS
####################################################################################################
class OpacityMenu(bpy.types.Operator):
    bl_idname = "pbr.showopacitymenu"
    bl_label = "Opaque"
    bl_description = "Set opacity mode"

    @staticmethod
    def execute(self, context):
        wm = context.window_manager
        wm.popup_menu(OpacityMenu.show_menu)
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        layout.operator(OpaqueMode.bl_idname)
        layout.operator(CutoutMode.bl_idname)
        layout.operator(FadeMode.bl_idname)


class OpaqueMode(bpy.types.Operator):
    bl_idname = "pbr.opaque"
    bl_label = "Opaque"
    bl_description = "opaque mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CLEAR')
        PBRPanel.MATERIALS['CURRENT'].opacity_mode = "Opaque"
        context.object.active_material.use_backface_culling = False
        context.object.active_material.blend_method = "OPAQUE"
        context.object.active_material.shadow_method = "OPAQUE"
        return {"FINISHED"}


class CutoutMode(bpy.types.Operator):
    bl_idname = "pbr.cutout"
    bl_label = "Cutout"
    bl_description = "cutout mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CLEAR')
        PBRPanel.MATERIALS['CURRENT'].opacity_mode = "Cutout"
        context.object.active_material.use_backface_culling = True
        context.object.active_material.blend_method = "CLIP"
        context.object.active_material.shadow_method = "CLIP"
        return {"FINISHED"}


class FadeMode(bpy.types.Operator):
    bl_idname = "pbr.fade"
    bl_label = "Fade"
    bl_description = "fade mode"

    @staticmethod
    def execute(self, context):
        update_opacity_add('CREATE')
        PBRPanel.MATERIALS['CURRENT'].opacity_mode = "Fade"
        context.object.active_material.use_backface_culling = True
        context.object.active_material.blend_method = "BLEND"
        context.object.active_material.shadow_method = "HASHED"
        return {"FINISHED"}


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
        location = (0,0)
        socket_name = ''
        node_name = nodes['Principled BSDF'].inputs['Alpha'].links[0].from_node.name
        if node_name == 'Albedo':
            socket_name = 'Alpha'
            if 'ORM' in PBRPanel.MATERIALS['CURRENT'].nodeslist:
                location = (-960, 520)
            else:
                location = (-360, 70)
        elif node_name == 'Opacity':
            socket_name = 'Color'
            location = (-700, -560)
        create_node("ShaderNodeMath", location, nodename="Opacity Add", operation="ADD", defaultinput=(1, 0), hide=True)
        link_nodes_in_a_row((FROM(node_name, socket_name), TO("Opacity Add", "Value")),
                            (FROM("Opacity Add", "Value"), TO("Principled BSDF", "Alpha")))
    return


####################################################################################################
# CHANGE PIPELINE CLASS
####################################################################################################
class PipelineMenu(bpy.types.Operator):
    bl_idname = "pbr.pipelinemenu"
    bl_label = "Change Pipeline"
    bl_description = "Set pipeline (ORM/MetalSmoothness/etc.)"

    @staticmethod
    def execute(self, context):
        wm = context.window_manager
        wm.popup_menu(PipelineMenu.show_menu, title="Found pipelines")
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        text = ''
        if PBRPanel.MATERIALS['CURRENT'].found["ORM"]:
            layout.operator(ORMTexturer.bl_idname, text="ORM")
            if PBRPanel.MATERIALS['CURRENT'].found["Color Mask"]:
                layout.operator(ORMMSKTexturer.bl_idname, text="ORM+MSK")
        if PBRPanel.MATERIALS['CURRENT'].found["Metal Smoothness"]:
            layout.operator(MetalSmoothnessTexturer.bl_idname, text="Metal Smoothness")
        if PBRPanel.MATERIALS['CURRENT'].found["Metal"] or PBRPanel.MATERIALS['CURRENT'].found["Roughness"]:
            if PBRPanel.MATERIALS['CURRENT'].found["Metal"] and PBRPanel.MATERIALS['CURRENT'].found["Roughness"]:
                text = "Metal+Roughness"
            elif PBRPanel.MATERIALS['CURRENT'].found["Metal"]:
                text = "Metal"
            elif PBRPanel.MATERIALS['CURRENT'].found["Roughness"]:
                text = "Roughness"
            layout.operator(MetalRoughnessTexturer.bl_idname, text=text)
        if not any(texture in PBRPanel.MATERIALS['CURRENT'].found for texture in
                   ["ORM", "Metal Smoothness", "Metal", "Roughness"]):
            layout.label(text="No options")


class DetailMaskMenu(bpy.types.Operator):
    bl_idname = "pbr.detailmaskmenu"
    bl_label = "Change Detail Map Source"
    bl_description = "Set sorce to put in Normal Mix node"

    @staticmethod
    def execute(self, context):
        wm = context.window_manager
        wm.popup_menu(DetailMaskMenu.show_menu, title="Available Detail Mask Sources:")
        return {"FINISHED"}

    def show_menu(self, context):
        layout = self.layout
        if PBRPanel.MATERIALS['CURRENT'].found["Detail Mask"]:
            layout.operator(DetailMaskSource.bl_idname, text="Detail Mask")
        if PBRPanel.MATERIALS['CURRENT'].found["Albedo"]:
            layout.operator(AlbedoAlphaSource.bl_idname, text="Albedo Alpha")
        layout.operator(NoneSource.bl_idname, text="None")


class DetailMaskSource(bpy.types.Operator):
    bl_idname = "pbr.detailmasksource"
    bl_label = "DetailMaskSource"
    bl_description = "Link Detail Mask to Normal Mix"

    @staticmethod
    def execute(self, context):
        link_nodes(FROM("Detail Mask", "Color"), TO("NormalMix", "Detail Mask"))
        PBRPanel.MATERIALS['CURRENT'].mask_source = "Detail Mask"
        return {"FINISHED"}


class AlbedoAlphaSource(bpy.types.Operator):
    bl_idname = "pbr.albedoalphasource"
    bl_label = "AlbedoAlphaSource"
    bl_description = "Link Albedo Alpha to Normal Mix"

    @staticmethod
    def execute(self, context):
        link_nodes(FROM("Albedo", "Alpha"), TO("NormalMix", "Detail Mask"))
        PBRPanel.MATERIALS['CURRENT'].mask_source = "Albedo Alpha"
        return {"FINISHED"}


class NoneSource(bpy.types.Operator):
    bl_idname = "pbr.nonesource"
    bl_label = "NoneSource"
    bl_description = "Remove Detail Mask link from Normal Mix"

    @staticmethod
    def execute(self, context):
        PBRPanel.MATERIALS['CURRENT'].mask_source = "None"
        nodes = context.object.active_material.node_tree
        if nodes.nodes['NormalMix'].inputs['Detail Mask'].links != ():
            nodes.links.remove(nodes.nodes['NormalMix'].inputs['Detail Mask'].links[0])
        return {"FINISHED"}


class MetalRoughnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metalroughness"
    bl_label = "MetalRoughness"
    bl_description = "Create Metal/Roughness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalRoughness")
        return {"FINISHED"}


class MetalSmoothnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metsm"
    bl_label = "Metal Sm."
    bl_description = "Create Metal Smothness Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("MetalSmoothness")
        return {"FINISHED"}


class ORMTexturer(bpy.types.Operator):
    bl_idname = "pbr.orm"
    bl_label = "ORM"
    bl_description = "Create ORM Pipeline"

    @staticmethod
    def execute(self, context):
        place_manual("ORM")
        return {"FINISHED"}


class ORMMSKTexturer(bpy.types.Operator):
    bl_idname = "pbr.ormmsk"
    bl_label = "ORM+MSK"
    bl_description = "Create ORM+MSK Pipeline"
    
    @staticmethod
    def execute(self, context):
        place_manual("ORM+MSK")
        return {"FINISHED"}


####################################################################################################
# SUBPANELS CLASSES
####################################################################################################
class TextureListPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_Textures"
    bl_space_type = "PROPERTIES"
    bl_label = "Found Textures"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        if not context.selected_objects:
            return False
        return PBRPanel.MATERIALS['CURRENT'].finished and context.active_object.active_material is not None

    def draw(self, context):
        layout = self.layout
        for texture in PBRPanel.MATERIALS['CURRENT'].found:
            if PBRPanel.MATERIALS['CURRENT'].found[texture]:
                row = layout.row()
                row.label(text=f"{texture}:")
                sub = row.row()
                sub.label(text=f"{PBRPanel.MATERIALS['CURRENT'].images[texture].name}")


class UVMapPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_UV"
    bl_space_type = "PROPERTIES"
    bl_label = "UV"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        if not bpy.context.selected_objects:
            return False
        return PBRPanel.MATERIALS['CURRENT'].finished and \
            context.active_object.active_material is not None and \
            len(bpy.data.meshes[bpy.context.active_object.data.name].uv_layers.keys()) > 1

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "UVMap", text="List of available UV Maps")


class TextureModePanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_TexturesMode"
    bl_space_type = "PROPERTIES"
    bl_label = "Found Textures"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        if not bpy.context.selected_objects:
            return False
        return PBRPanel.MATERIALS['CURRENT'].finished and context.active_object.active_material is not None

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if not PBRPanel.MATERIALS['CURRENT'].nodeslist:
            row.label(text="Mode: None")
        else:
            row.label(text=get_mode())
        row = layout.row()
        row.operator(PipelineMenu.bl_idname)


class TexturePropsPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_TexturesProps"
    bl_space_type = "PROPERTIES"
    bl_label = "Texture Properties"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        if not context.selected_objects:
            return False
        return PBRPanel.MATERIALS['CURRENT'].finished and context.active_object.active_material is not None

    def draw(self, context):
        material_prop = bpy.context.active_object.active_material.props
        layout = self.layout
        if not PBRPanel.MATERIALS['CURRENT'].found["Albedo"]:
            row = layout.row()
            row.prop(material_prop, "AlbedoColor")
        if "Normal Map" in PBRPanel.MATERIALS['CURRENT'].nodeslist:
            row = layout.row()
            row.prop(material_prop, "NormaMaplStrength")
            row = layout.row()
            row.prop(material_prop, "NormalMapInverterEnabled")
            if "NormalMix" in bpy.context.object.active_material.node_tree.nodes:
                row = layout.row()
                row.prop(material_prop, "DetailMapInvertorEnabled")
                if "Detail Mask" not in PBRPanel.MATERIALS['CURRENT'].nodeslist and PBRPanel.MATERIALS['CURRENT'].mask_source == "None":
                    row = layout.row()
                    row.prop(material_prop, "DetailMaskStrength")
                row = layout.row()
                row.operator(DetailMaskMenu.bl_idname)
                row = layout.row()
        TexturePropsPanel.show_prop(context, layout, ["Metal", "ORM", "Metal Smoothness"], ["MetallicAdd"])
        TexturePropsPanel.show_prop(context, layout, ["Roughness", "ORM", "Metal Smoothness"], ["RoughnessAdd"])
        TexturePropsPanel.show_prop(context, layout, ["Emission"], ["EmissionMult"])
        TexturePropsPanel.show_prop(context, layout, ["ORM", "Occlusion"], ["AO_Strength"])
        TexturePropsPanel.show_prop(context, layout, ["Specular"], ["SpecularAdd"])
        TexturePropsPanel.show_prop(context, layout, ["Color Mask"], ["MixR", "MixG", "MixB"], header="Color mask settings:")

    @staticmethod
    def show_prop(context, layout, textures, properties, header=""):
        material_prop = context.active_object.active_material.props
        if any(texture in PBRPanel.MATERIALS['CURRENT'].nodeslist for texture in textures):
            if header != "":
                row = layout.row()
                row.label(text=header)
            for prop in properties:
                row = layout.row()
                row.prop(material_prop, prop)


class TextureCoordinatesPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_TexturesCoordinates"
    bl_space_type = "PROPERTIES"
    bl_label = "Texture Coordinates"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        if not bpy.context.selected_objects:
            return False
        return PBRPanel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material is not None and \
            "Mapping" in context.object.active_material.node_tree.nodes

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        layout = self.layout
        for prop in ["Location", "Rotation", "Scale"]:
            row = layout.row()
            row.prop(material_prop, prop)


class DetailMapCoordinatesPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_DetailMapCoordinates"
    bl_space_type = "PROPERTIES"
    bl_label = "Detail Map Coordinates"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        if not context.selected_objects:
            return False
        return PBRPanel.MATERIALS['CURRENT'].finished and context.active_object.active_material is not None and \
            "Detail Mapping" in context.object.active_material.node_tree.nodes

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        layout = self.layout
        for prop in ["DetailMapLocation", "DetailMapRotation", "DetailMapScale"]:
            row = layout.row()
            row.prop(material_prop, prop)


class OpacityPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_opacity_mode"
    bl_space_type = "PROPERTIES"
    bl_label = "Opacity Settings"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(cls, context):
        if 'CURRENT' in PBRPanel.MATERIALS:
            return (PBRPanel.MATERIALS['CURRENT'].opacity_from_albedo or PBRPanel.MATERIALS['CURRENT'].found["Opacity"]) and \
                   PBRPanel.MATERIALS['CURRENT'].finished and \
                   context.active_object.active_material is not None and \
                   context.selected_objects != []
        return False

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Opacity Mode:")
        row.operator(OpacityMenu.bl_idname, text=PBRPanel.MATERIALS['CURRENT'].opacity_mode)
        material_prop = context.active_object.active_material.props
        if PBRPanel.MATERIALS['CURRENT'].opacity_mode == "Cutout":
            row = layout.row()
            row.prop(context.active_object.active_material.props, "AlphaThreshold")
        if PBRPanel.MATERIALS['CURRENT'].opacity_mode == "Fade":
            row = layout.row()
            row.prop(material_prop, "AlphaMode")
            row = layout.row()
            row.prop(material_prop, "OpacityAdd")


####################################################################################################
# TEXTURE GETTER CLASS
####################################################################################################
class GetTextureOperator(bpy.types.Operator):
    bl_idname = "textures.get"
    bl_label = "Assign Textures"
    bl_description = "Assign files with textures using choosen name pattern"

    @staticmethod
    def execute(self, context):
        clear_images()
        PBRPanel.MATERIALS['CURRENT'].reset()
        path = context.active_object.active_material.props.conf_path
        filenames = next(os.walk(path), (None, None, []))[2]
        for file in filenames:
            GetTextureOperator.get_texture(file)
        PBRPanel.MATERIALS['CURRENT'].finished = True
        place_automatic()
        return {"FINISHED"}

    @staticmethod
    def get_texture(file):
        threshold = 0
        title = ''

        if file.split(".")[-1].lower() == 'meta':
            return False

        name = file.lower().split(".")[0]
        pattern = bpy.context.active_object.active_material.props.texture_pattern.lower().split("-")

        if len(pattern) > 1:
            pattern, skip = pattern[0].strip(), pattern[1].strip()
        else:
            pattern, skip = pattern[0].strip(), None
        if skip is not None and skip in name:
            return False

        for texture in TEXTURES:
            for mask in TEXTURES_MASK[texture]:
                if name.endswith(mask.lower()):
                    if len(mask.lower()) > threshold:
                        threshold = len(mask.lower())
                        title = texture
                        break

        if threshold != 0 and pattern in name:
            if file in bpy.data.images:
                bpy.data.images.remove(bpy.data.images[file])
            image = bpy.data.images.load(
                filepath=os.path.join(bpy.context.active_object.active_material.props.conf_path, file))

            if not any(title == colored for colored in ["Albedo", "Emission", "Specular", "Occlusion"]):
                image.colorspace_settings.name = "Non-Color"
            PBRPanel.MATERIALS['CURRENT'].found[title], PBRPanel.MATERIALS['CURRENT'].images[title] = True, image
        return True


####################################################################################################
# MAIN PANEL CLASS
####################################################################################################
class PBRPanel(bpy.types.Panel):
    bl_label = "Easy PBR Hook"
    bl_idname = "PBR_PT_Core"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    current_path = ""
    current_pattern = ""
    MATERIALS = {}

    @classmethod
    def poll(cls, context):
        return context.active_object.active_material is not None

    def draw(self, context):
        material_prop = context.active_object.active_material.props
        PBRPanel.current_path = material_prop.conf_path
        PBRPanel.current_pattern = material_prop.texture_pattern
        layout = self.layout
        if PBRPanel.is_bad_state(layout):
            return
        PBRPanel.update_material()
        row = layout.row()
        row.prop(material_prop, "conf_path")
        row = layout.row()
        row.prop(material_prop, "texture_pattern")
        PBRPanel.assign_textures(layout)

    @staticmethod
    def update_material():
        material_name = bpy.context.selected_objects[0].active_material.name
        if 'CURRENT' not in PBRPanel.MATERIALS:
            Material(material_name)
        elif PBRPanel.MATERIALS['CURRENT'].name != material_name:
            if material_name not in PBRPanel.MATERIALS:
                Material(material_name)
            else:
                PBRPanel.MATERIALS['CURRENT'] = PBRPanel.MATERIALS[material_name]

    @staticmethod
    def is_bad_state(layout):
        if not bpy.context.selected_objects:
            row = layout.row()
            row.label(text="No object")
            return True
        if bpy.context.selected_objects[0].active_material is None:
            row = layout.row()
            row.label(text="No material")
            PBRPanel.MATERIALS['CURRENT'].finished = False
            return True
        return False

    @staticmethod
    def assign_textures(layout):
        row = layout.row()
        text = "Reassign textures" if PBRPanel.MATERIALS['CURRENT'].finished else "Assign textures"
        row.operator(GetTextureOperator.bl_idname, text=text)


####################################################################################################
# CLASSES LIST, REGISTER AND RUN
####################################################################################################
modules = [PBRPanel, UVMapProp, MaterialProps, GetTextureOperator, PipelineMenu,
           ORMTexturer, MetalSmoothnessTexturer, MetalRoughnessTexturer, ORMMSKTexturer,
           FadeMode, OpaqueMode, CutoutMode, OpacityMenu, UVMapPanel, TextureListPanel, TextureModePanel,
           TexturePropsPanel, DetailMaskMenu, DetailMaskSource, AlbedoAlphaSource, NoneSource,
           TextureCoordinatesPanel, DetailMapCoordinatesPanel, OpacityPanel]


def register():
    for module in modules:
        bpy.utils.register_class(module)


def unregister():
    for module in modules:
        bpy.utils.unregister_class(module)


if __name__ == "__main__":
    register()
