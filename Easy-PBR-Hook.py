import bpy
import os
####################################################################################################
#CREDITS
####################################################################################################
bl_info = {
    "name": "Easy PBR Hook",
    "author": "Dmitry F.",
    "version": (1, 4, 11),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Easy PBR Hook",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Material",
}
####################################################################################################
#MATERIAL CLASS
####################################################################################################
class Material():
    def __init__(self, name):
        self.name = name
        PBR_Panel.MATERIALS[name] = self
        PBR_Panel.MATERIALS['CURRENT'] = self
        self.found = dict.fromkeys(TEXTURES, False)
        self.images = dict.fromkeys(TEXTURES, None)
        self.nodeslist = []
        self.opacity_mode = "Opaque"
        self.opacity_from_albedo = False
        self.finished = False
        self.automatic = True

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
####################################################################################################
#TEXTURES MASK
####################################################################################################
TEXTURES_MASK = {"Albedo": ("basecolor", "base_color", "bc", "color", "albedo", "albedotransparency", "albedo_transparency", "diffuse", "diffusemap", "diffuse_map", "alb"),
                 "Metal Smoothness": ("metsm", "met_sm", "metal_smoothness", "metalic_smoothness", "metalsmoothness", "metallicsmoothness","metal_smooth", "metalsmooth", "metsmooth"),
                 "Metal": ("met", "metal", "_m", "metall", "metallic"),
                 "Roughness": ("_r", "rough", "roughness"),
                 "ORM": ("_orm", "occlusionroughnessmetallic"),
                 "Color Mask": ("_m", "msk", "colormask", "color_mask"),
                 "Normal Map": ("normal", "nm", "_n", "normal_map", "normalmap", "normaldx", "normal_dx", "nrm"),
                 "Emission": ("_e", "emis", "emiss", "emission"),
                 "Specular": ("_s", "specular", "spec"),
                 "Occlusion": ("occlusion", "_ao", "ambientocclusion"),
                 "Displacement": ("displacement", "height", "hightmap"),
                 "Opacity": ("opacity", "transparency")}

TEXTURES = list(TEXTURES_MASK.keys())
####################################################################################################
#PROPS CLASS AND ITS UPDATE
####################################################################################################
class MaterialProps(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Material.props = bpy.props.PointerProperty(name="Custom properties", description="Custom Properties for Material", type=cls)

        cls.RoughnessAdd = bpy.props.FloatProperty(name="Roughness", min = 0, max = 1, update = lambda a,b: updateFloat(a,b,"Roughness"))
        cls.MetallicAdd = bpy.props.FloatProperty(name = "Metallic", min = 0, max = 1, update = lambda a,b: updateFloat(a,b,"Metallic"))
        cls.SpecularAdd = bpy.props.FloatProperty(name = "Specular", min = 0, max = 100, update = lambda a,b: updateFloat(a,b,"Specular"))
        cls.EmissionMult = bpy.props.FloatProperty(name = "Emission", min = 0, max = 1, update = lambda a,b: updateFloat(a,b,"Emission"))
        cls.NormaMaplStrength = bpy.props.FloatProperty(name = "Normal Strength", min = 0, update = lambda a,b: updateFloat(a,b,"Normal Strength"))
        cls.AO_Strength = bpy.props.FloatProperty(name = "AO Strength", min = 0, max = 1, update = lambda a,b: updateFloat(a,b,"AO Strength"))
        cls.AlphaTreshold = bpy.props.FloatProperty(name = "Alpha Treshold", min = 0, max = 1, update = lambda a,b: updateFloat(a,b,"Alpha Treshold"))

        cls.NormalMapInvertorEnabled = bpy.props.BoolProperty(name = "Invert", update=updateNormal)

        cls.MixR = bpy.props.FloatVectorProperty(name = "Red сhannel", subtype = "COLOR", size = 4, min = 0, max = 1, update=updateColor)
        cls.MixG = bpy.props.FloatVectorProperty(name = "Green сhannel", subtype = "COLOR", size = 4, min = 0, max = 1, update=updateColor)
        cls.MixB = bpy.props.FloatVectorProperty(name = "Blue сhannel", subtype = "COLOR", size = 4, min = 0, max = 1, update=updateColor)
        cls.AlbedoColor = bpy.props.FloatVectorProperty(name = "Albedo Color", subtype = "COLOR", size = 4, min = 0, max = 1, update=updateColor)

        cls.conf_path = bpy.props.StringProperty(
            name = "Path to textures", default = "",  description = "Sets the path to texture folder",
            subtype = "DIR_PATH", update=updateString)
        cls.texture_pattern = bpy.props.StringProperty(
            name = "Keyword", default = "",
            description = "Keyword to find specific texture pack. You can use '-' to describe skip keyword",
            update=updateString)

        cls.Location = bpy.props.FloatVectorProperty(name = "Location", subtype = 'XYZ', update=lambda a,b: updateFloat(a,b,"Location"))
        cls.Rotation = bpy.props.FloatVectorProperty(name = "Rotation", subtype = 'EULER', update=lambda a,b: updateFloat(a,b,"Rotation"))
        cls.Scale = bpy.props.FloatVectorProperty(name = "Scale", subtype = 'XYZ', update=lambda a,b: updateFloat(a,b,"Scale"))

        cls.AlphaMode = bpy.props.EnumProperty(items=[('STRAIGHT', 'Straight', ''), ('CHANNEL_PACKED', 'Channel Packed', '')], update=updateAlpha)
        cls.OpacityAdd = bpy.props.FloatProperty(name = "Opacity", min = 0, max = 1, update=lambda a,b: updateFloat(a,b,"Opacity"))

        bpy.types.Scene.UVMap = bpy.props.EnumProperty(items=UV_items, update=updateUV)
        bpy.types.Scene.test_collection = bpy.props.CollectionProperty(type=UVMapProp)

    @classmethod
    def unregister(cls):
        del bpy.types.Material.props

def updateFloat(self, context, origin=""):
    nodes = bpy.context.object.active_material.node_tree.nodes
    MaterialProps = bpy.context.active_object.active_material.props
    if origin == "Roughness" and "Roughness Add" in nodes:
        nodes["Roughness Add"].inputs[1].default_value = MaterialProps.RoughnessAdd - 1
    elif origin == "Metallic" and "Metallic Add" in nodes:
        nodes["Metallic Add"].inputs[1].default_value = MaterialProps.MetallicAdd - 1
    elif origin == "Specular" and "Specular Add" in nodes:
        nodes["Specular Add"].inputs[1].default_value = MaterialProps.SpecularAdd
    elif origin == "Emission" and "Emission Multiply" in nodes:
        nodes["Emission Multiply"].inputs[1].default_value = MaterialProps.EmissionMult
    elif origin == "Normal Strength" and "Normal Map Strength" in nodes:
        nodes["Normal Map Strength"].inputs["Strength"].default_value = MaterialProps.NormaMaplStrength
    elif origin == "AO Strength" and all(AO in nodes for AO in ["AO_Mult_Albedo", "AO_Mult_Spec"]):
        nodes["AO_Mult_Albedo"].inputs[0].default_value = nodes["AO_Mult_Spec"].inputs[0].default_value = MaterialProps.AO_Strength
    elif origin == "Alpha Treshold":
        if bpy.context.object.active_material.blend_method != "OPAQUE":
            bpy.context.object.active_material.alpha_threshold = MaterialProps.AlphaTreshold
    elif origin == "Location" and "Mapping" in nodes:
        nodes["Mapping"].inputs["Location"].default_value = MaterialProps.Location
    elif origin == "Rotation" and "Mapping" in nodes:
        nodes["Mapping"].inputs["Rotation"].default_value = MaterialProps.Rotation
    elif origin == "Scale" and "Mapping" in nodes:
        nodes["Mapping"].inputs["Scale"].default_value = MaterialProps.Scale
    elif origin == "Opacity":
        nodes["Opacity Add"].inputs[1].default_value = MaterialProps.OpacityAdd

def updateNormal(self, context):
    MaterialProps = bpy.context.active_object.active_material.props
    if "Normal Map" in PBR_Panel.MATERIALS['CURRENT'].nodeslist:
        if MaterialProps.NormalMapInvertorEnabled:
            PlaceNormalMapMapInvertor()
        else:
            RemoveNormalMapInvertor()

def PlaceNormalMapMapInvertor():
    if "NormalMapInvertor" not in bpy.data.node_groups:
        CreateNormalMapInvertor()
    CreateNode("ShaderNodeGroup", (-360, -650), nodename="NormalMapInvertor", nodegroup="NormalMapInvertor", hide=True)
    LinkNodesInARow( (FROM("Normal Map", "Color"), TO("NormalMapInvertor", "NM Input")), (FROM("NormalMapInvertor", "NM Output"), TO("Normal Map Strength", "Color")) )

def RemoveNormalMapInvertor():
    nodes = bpy.context.object.active_material.node_tree.nodes
    if "NormalMapInvertor" in nodes:
        nodes.remove(nodes["NormalMapInvertor"])
        LinkNodes( FROM("Normal Map", "Color"), TO("Normal Map Strength", "Color") )

def updateColor(self, context):
    nodes = bpy.context.object.active_material.node_tree.nodes
    MaterialProps = bpy.context.active_object.active_material.props
    if "Albedo" in PBR_Panel.MATERIALS['CURRENT'].nodeslist and nodes["Albedo"].type == "RGB":
        nodes["Albedo"].outputs["Color"].default_value  = MaterialProps.AlbedoColor
    else:
        nodes["Principled BSDF"].inputs["Base Color"].default_value  = MaterialProps.AlbedoColor
    if "Color Mask" in PBR_Panel.MATERIALS['CURRENT'].nodeslist:
        nodes["RedColor"].outputs["Color"].default_value  = MaterialProps.MixR
        nodes["GreenColor"].outputs["Color"].default_value = MaterialProps.MixG
        nodes["BlueColor"].outputs["Color"].default_value = MaterialProps.MixB

def updateString(self, context):
    if bpy.context.active_object.active_material.props.conf_path != bpy.path.abspath(bpy.context.active_object.active_material.props.conf_path):
        bpy.context.active_object.active_material.props.conf_path = bpy.path.abspath(bpy.context.active_object.active_material.props.conf_path)
    if PBR_Panel.current_path != bpy.context.active_object.active_material.props.conf_path or PBR_Panel.current_pattern != bpy.context.active_object.active_material.props.texture_pattern:
        PBR_Panel.MATERIALS['CURRENT'].finished = False

def updateAlpha(self, context):
    MaterialProps = bpy.context.active_object.active_material.props
    bpy.data.images[PBR_Panel.MATERIALS['CURRENT'].images['Albedo'].name].alpha_mode = MaterialProps.AlphaMode

def updateUV(self, context):
    nodes = bpy.context.object.active_material.node_tree.nodes
    nodes["UVMap"].uv_map = bpy.context.scene.UVMap

def resetProps():
    prop = bpy.context.active_object.active_material.props
    prop.RoughnessAdd = 1
    prop.MetallicAdd = 1
    prop.SpecularAdd = 1
    prop.EmissionMult = 1
    prop.NormaMaplStrength = 1
    prop.AO_Strength = 1
    prop.AlphaTreshold = 0
    prop.NormalMapInvertorEnabled = False
    prop.MixR = (1,1,1,1)
    prop.MixG = (1,1,1,1)
    prop.MixB = (1,1,1,1)
    prop.Location = (0,0,0)
    prop.Rotation = (0,0,0)
    prop.Scale = (1,1,1)
    prop.OpacityAdd = 0

def resetColors():
    nodes = bpy.context.object.active_material.node_tree.nodes
    nodes["RedColor"].outputs["Color"].default_value = (1,1,1,1)
    nodes["GreenColor"].outputs["Color"].default_value = (1,1,1,1)
    nodes["BlueColor"].outputs["Color"].default_value = (1,1,1,1)

class UVMapProp(bpy.types.PropertyGroup):
    uv: bpy.props.StringProperty()

def UV_items(self, context):
    Enum_items = []
    for UV in bpy.data.meshes[context.active_object.name].uv_layers.keys():
        data = str(UV)
        item = (data, data, '')
        Enum_items.append(item)
    return Enum_items
####################################################################################################
#NODE FUNCTIONS
####################################################################################################
def CreateNode(nodetype, location, nodename="", blendtype="", operation="", nodegroup=None, image=None, hide=False, defaultinput=None, nodetree="default"):
    nodes = bpy.context.object.active_material.node_tree.nodes if nodetree=="default" else nodetree.nodes
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
    newnode.hide=hide

def LinkNodes(FROM, TO, nodetree="default"):
    node_tree = bpy.context.object.active_material.node_tree if nodetree=="default" else nodetree
    node_tree.links.new(node_tree.nodes[FROM[0]].outputs[FROM[1]], node_tree.nodes[TO[0]].inputs[TO[1]])

def LinkNodesInARow(*routes, nodetree="default"):
    [LinkNodes((route[0][0], route[0][1]), (route[1][0], route[1][1]), nodetree) for route in routes]

def FROM(name, socket):
    return [name, socket]

def TO(name, socket):
    return [name,socket]

def CreateSockets(node, *sockets, socket=""):
    node_sockets = node.inputs if socket=="INPUT" else node.outputs
    [node_sockets.new(sockettype, socket) for sockettype, socket in sockets]
####################################################################################################
#CREATING NODE GROUPS
####################################################################################################
def CreateNormalMapInvertor():
    NormalMapInvert = bpy.data.node_groups.new("NormalMapInvertor", "ShaderNodeTree")
    NormalMapInvert.name = "NormalMapInvertor"
    CreateSockets(NormalMapInvert, ("NodeSocketImage","NM Input"), socket="INPUT")
    CreateSockets(NormalMapInvert, ("NodeSocketImage","NM Output"), socket="OUTPUT")
    CreateNode("NodeGroupInput", (-300,0), nodename="Group Input", hide=True, nodetree=NormalMapInvert)
    CreateNode("NodeGroupOutput", (340,0), nodename="Group Output", hide=True, nodetree=NormalMapInvert)
    CreateNode("ShaderNodeSeparateRGB", (-140,0), nodename="Separate RGB", hide=True, nodetree=NormalMapInvert)
    CreateNode("ShaderNodeCombineRGB", (180,0), nodename="Combine RGB", hide=True, nodetree=NormalMapInvert)
    CreateNode("ShaderNodeInvert", (20,0), nodename="Invert", hide=True, nodetree=NormalMapInvert)
    LinkNodesInARow( (FROM("Group Input", "NM Input"), TO("Separate RGB", "Image")), (FROM("Separate RGB", "R"), TO("Combine RGB", "R")),
                     (FROM("Separate RGB", "B"), TO("Combine RGB", "B")), (FROM("Separate RGB", "G"), TO("Invert", "Color")),
                     (FROM("Invert", "Color"), TO("Combine RGB", "G")), (FROM("Combine RGB", "Image"), TO("Group Output", "NM Output")), nodetree=NormalMapInvert)

def CreateNormalMix():
    NormalMix = bpy.data.node_groups.new("NormalMix", "ShaderNodeTree")
    NormalMix.name = "NormalMix"
    CreateSockets(NormalMix, ("NodeSocketImage","Main"), ("NodeSocketImage","Detail"), ("NodeSocketFloat","Detail Mask"), socket="INPUT")
    CreateSockets(NormalMix, ("NodeSocketImage","Color"), socket="OUTPUT")
    CreateNode("NodeGroupInput", (0,-40), nodename="Group Input", hide=True, nodetree=NormalMix)
    CreateNode("NodeGroupOutput", (1400,-36), nodename="Group Output", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeSeparateRGB", (200,0), nodename="Separate RGB (1)", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeSeparateRGB", (200,-75), nodename="Separate RGB (2)", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeSeparateRGB", (1000,-36), nodename="Separate RGB (3)", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeCombineRGB", (400,0), nodename="Combine RGB (1)", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeCombineRGB", (400,-75), nodename="Combine RGB (2)", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeCombineRGB", (1200,-36), nodename="Combine RGB (3)", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeMixRGB", (800,-36), nodename="Subtract", blendtype="SUBTRACT", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeMixRGB", (600,-36), nodename="Add", blendtype="ADD", hide=True, nodetree=NormalMix)
    CreateNode("ShaderNodeMath", (400, -36), nodename="Multiply", operation="MULTIPLY", hide=True, nodetree=NormalMix)
    LinkNodesInARow( (FROM("Group Input", "Main"), TO("Separate RGB (1)", "Image")), (FROM("Group Input", "Detail"), TO("Separate RGB (2)", "Image")),
                     (FROM("Separate RGB (1)", "R"), TO("Combine RGB (1)", "R")), (FROM("Separate RGB (1)", "G"), TO("Combine RGB (1)", "G")),
                     (FROM("Separate RGB (2)", "R"), TO("Combine RGB (2)", "R")), (FROM("Separate RGB (2)", "G"), TO("Combine RGB (2)", "G")),
                     (FROM("Separate RGB (1)", "B"), TO("Multiply", 0)), (FROM("Separate RGB (2)", "B"), TO("Multiply", 1)),
                     (FROM("Combine RGB (1)", "Image"), TO("Add", "Color1")), (FROM("Combine RGB (2)", "Image"), TO("Add", "Color2")), (FROM("Group Input", "Detail Mask"), TO("Add", "Fac")),
                     (FROM("Group Input", "Detail Mask"), TO("Subtract", "Fac")), (FROM("Add", "Color"), TO("Subtract", "Color1")), (FROM("Subtract", "Color"), TO("Separate RGB (3)", "Image")),
                     (FROM("Multiply", "Value"), TO("Combine RGB (3)", "B")), (FROM("Separate RGB (3)", "R"), TO("Combine RGB (3)", "R")), (FROM("Separate RGB (3)", "G"), TO("Combine RGB (3)", "G")),
                     (FROM("Combine RGB (3)", "Image"), TO("Group Output", "Color")), nodetree=NormalMix)
####################################################################################################
#PLACE FUNCTIONS
####################################################################################################
def ClearMaterial():
    nodes = bpy.context.object.active_material.node_tree.nodes
    bpy.context.object.active_material.use_backface_culling = False
    [nodes.remove(nodes[node]) for node in nodes.keys()]
    CreateNode("ShaderNodeBsdfPrincipled", (0, 0))
    CreateNode("ShaderNodeOutputMaterial", (300, 0))
    LinkNodes(FROM("Principled BSDF", "BSDF"), TO("Material Output", "Surface"))

def ClearImages():
    if len(bpy.data.materials)<=2:
        nodes = bpy.context.object.active_material.node_tree.nodes
        for node in nodes.keys():
            if hasattr(nodes[node], "image"):
                if nodes[node].image != None:
                    bpy.data.images.remove(nodes[node].image)

def PlaceBase():
    nodes = bpy.context.object.active_material.node_tree.nodes
    ClearMaterial()
    if "Albedo" not in nodes:
        PlaceAlbedo()
    if "Normal Map" not in nodes:
        PlaceNormalMap()
    if "Emission" not in nodes:
        PlaceEmission()
    if "Specular" not in nodes:
        PlaceSpecular()
    if "Displacement" not in nodes:
        PlaceDisplacement()
    if "Opacity" not in nodes:
        PlaceOpacity()

def PlaceAlbedo():
    if PBR_Panel.MATERIALS['CURRENT'].found["Albedo"]:
        CreateNode("ShaderNodeTexImage", (-700, 300), nodename="Albedo", image=PBR_Panel.MATERIALS['CURRENT'].images["Albedo"])
        LinkNodes( FROM("Albedo", "Color"), TO("Principled BSDF", "Base Color") )
        if PBR_Panel.MATERIALS['CURRENT'].images["Albedo"].name.lower().split(".")[0].endswith("transparency"):
            LinkNodes( FROM("Albedo", "Alpha"), TO("Principled BSDF", "Alpha") )
            PBR_Panel.MATERIALS['CURRENT'].opacity_from_albedo = True
    elif PBR_Panel.MATERIALS['CURRENT'].found["ORM"] or PBR_Panel.MATERIALS['CURRENT'].found["Occlusion"]:
        CreateNode("ShaderNodeRGB", (-700, 300), nodename="Albedo")
    else:
        return
    CheckAndAddToNodesList("Albedo")

def PlaceNormalMap():
    if PBR_Panel.MATERIALS['CURRENT'].found["Normal Map"]:
        CreateNode("ShaderNodeTexImage", (-700, -600), nodename="Normal Map", image=PBR_Panel.MATERIALS['CURRENT'].images["Normal Map"])
        CreateNode("ShaderNodeNormalMap", (-360, -600), nodename="Normal Map Strength", hide=True)
        LinkNodesInARow( (FROM("Normal Map", "Color"), TO("Normal Map Strength", "Color")), (FROM("Normal Map Strength", "Normal"), TO("Principled BSDF", "Normal")) )
        CheckAndAddToNodesList("Normal Map")

def PlaceEmission():
    if PBR_Panel.MATERIALS['CURRENT'].found["Emission"]:
        CreateNode("ShaderNodeTexImage", (-700, -300), nodename="Emission", image=PBR_Panel.MATERIALS['CURRENT'].images["Emission"])
        CreateNode("ShaderNodeMath", (-360, -300), nodename="Emission Multiply", operation="MULTIPLY", hide=True)
        LinkNodesInARow( (FROM("Emission", "Color"), TO("Emission Multiply", "Value")), (FROM("Emission Multiply", "Value"), TO("Principled BSDF", "Emission")) )
        CheckAndAddToNodesList("Emission")

def PlaceSpecular():
    if PBR_Panel.MATERIALS['CURRENT'].found["Specular"]:
        CreateNode("ShaderNodeTexImage", (-700, -1200), nodename="Specular", image=PBR_Panel.MATERIALS['CURRENT'].images["Specular"])
        CreateNode("ShaderNodeMath", (-360, -1200), nodename="Specular Add", operation="ADD", hide=True)
        LinkNodesInARow( (FROM("Specular", "Color"), TO("Specular Add", "Value")), (FROM("Specular Add", "Value"), TO("Principled BSDF", "Specular")) )
        CheckAndAddToNodesList("Specular")

def PlaceOcclusion():
    if PBR_Panel.MATERIALS['CURRENT'].found["Occlusion"]:
        nodes = bpy.context.object.active_material.node_tree.nodes
        CreateNode("ShaderNodeTexImage", (-1000, 300), nodename="Occlusion", image=PBR_Panel.MATERIALS['CURRENT'].images["Occlusion"])
        CreateNode("ShaderNodeMixRGB", (-360, 220), nodename="AO_Mult_Albedo", blendtype="MULTIPLY", defaultinput=("Fac", 1), hide=True)
        CreateNode("ShaderNodeMixRGB", (-360, 170), nodename="AO_Mult_Spec", blendtype="MULTIPLY", defaultinput=("Fac", 1), hide=True)
        if PBR_Panel.MATERIALS['CURRENT'].found["Specular"]:
            LinkNodesInARow( (FROM("Specular", "Color"), TO("Specular Add", "Value")), (FROM("Specular Add", "Value"), TO("AO_Mult_Spec", "Color1")) )
            nodes["Specular Add"].location = (-360, 50)
            nodes["Specular"].location = (-1000, 0)
        else:
            CreateNode("ShaderNodeValue", (-360, 120), nodename="Specular Value", hide=True)
            LinkNodes( FROM("Specular Value", "Value"), TO("AO_Mult_Spec", "Color1") )

        LinkNodesInARow( (FROM("Occlusion", "Color"), TO("AO_Mult_Albedo", "Color2")), (FROM("Occlusion", "Color"), TO("AO_Mult_Spec", "Color2")),
                         (FROM("Albedo", "Color"), TO("AO_Mult_Albedo", "Color1")), (FROM("AO_Mult_Albedo", "Color"), TO("Principled BSDF", "Base Color")),
                         (FROM("AO_Mult_Spec", "Color"), TO("Principled BSDF", "Specular")) )
        CheckAndAddToNodesList("Occlusion")

def PlaceDisplacement():
    if PBR_Panel.MATERIALS['CURRENT'].found["Displacement"]:
        CreateNode("ShaderNodeTexImage", (-700, -900), nodename="Displacement", image=PBR_Panel.MATERIALS['CURRENT'].images["Displacement"])
        CreateNode("ShaderNodeDisplacement", (-360, -900), nodename="Normal Displacement", hide=True)
        LinkNodesInARow( (FROM("Displacement", "Color"), TO("Normal Displacement", "Normal")), (FROM("Normal Displacement", "Displacement"), TO("Material Output", "Displacement")) )
        CheckAndAddToNodesList("Displacement")

def PlaceOpacity():
    if PBR_Panel.MATERIALS['CURRENT'].found["Opacity"]:
        CreateNode("ShaderNodeTexImage", (-1000, -600), nodename="Opacity", image=PBR_Panel.MATERIALS['CURRENT'].images["Opacity"])
        LinkNodes( FROM("Opacity", "Color"), TO("Principled BSDF", "Alpha") )
        CheckAndAddToNodesList("Opacity")

def PlaceORMMSK():
    PlaceORM()
    PlaceColorMask()

def PlaceORM():
    PlaceBase()
    CreateNode("ShaderNodeTexImage", (-1000, 0), nodename="ORM", image=PBR_Panel.MATERIALS['CURRENT'].images["ORM"])
    CreateNode("ShaderNodeSeparateRGB", (-700, 0), nodename="SeparateORM", hide=True)
    CreateNode("ShaderNodeMixRGB", (-360, 220), nodename="AO_Mult_Albedo", blendtype="MULTIPLY", defaultinput=("Fac", 1), hide=True)
    CreateNode("ShaderNodeMixRGB", (-360, 170), nodename="AO_Mult_Spec", blendtype="MULTIPLY", defaultinput=("Fac", 1), hide=True)
    CreateNode("ShaderNodeMath", (-360, 0), nodename="Metallic Add", operation="ADD", hide=True)
    CreateNode("ShaderNodeMath", (-360, -50), nodename="Roughness Add", operation="ADD", hide=True)

    if PBR_Panel.MATERIALS['CURRENT'].found["Specular"]:
        LinkNodes( FROM("Specular", "Color"), TO("Specular Add", "Value") )
        LinkNodes( FROM("Specular Add", "Value"), TO("AO_Mult_Spec", "Color1") )
        nodes = bpy.context.object.active_material.node_tree.nodes
        nodes["Specular Add"].location = (-700, 350)
        nodes["Specular"].location = (-1000, 300)
    else:
        CreateNode("ShaderNodeValue", (-360, 120), nodename="Specular Value", hide=True)
        LinkNodes(FROM("Specular Value", "Value"), TO("AO_Mult_Spec", "Color1"))
    LinkNodesInARow( (FROM("ORM", "Color"), TO("SeparateORM", "Image")), (FROM("SeparateORM", "G"), TO("Roughness Add", "Value")),
                     (FROM("Roughness Add", "Value"), TO("Principled BSDF", "Roughness")), (FROM("SeparateORM", "B"), TO("Metallic Add", "Value")),
                     (FROM("Metallic Add", "Value"), TO("Principled BSDF", "Metallic")), (FROM("SeparateORM", "R"), TO("AO_Mult_Spec", "Color2")),
                     (FROM("SeparateORM", "R"), TO("AO_Mult_Albedo", "Color2")), (FROM("Albedo", "Color"), TO("AO_Mult_Albedo", "Color1")),
                     (FROM("AO_Mult_Albedo", "Color"), TO("Principled BSDF", "Base Color")), (FROM("AO_Mult_Spec", "Color"), TO("Principled BSDF", "Specular")) )
    CheckAndAddToNodesList("ORM")

def PlaceColorMask():
    nodes = bpy.context.object.active_material.node_tree.nodes
    CreateNode("ShaderNodeTexImage", (-1300, 300), nodename="Color Mask", image=PBR_Panel.MATERIALS['CURRENT'].images["Color Mask"])
    CreateNode("ShaderNodeSeparateRGB", (-1200, 333), nodename="SeparateMSK", hide=True)
    CreateNode("ShaderNodeMixRGB", (-970, 570), nodename="MixRed", blendtype="MULTIPLY", hide=True)
    CreateNode("ShaderNodeMixRGB", (-770, 570), nodename="MixGreen", blendtype="MULTIPLY", hide=True)
    CreateNode("ShaderNodeMixRGB", (-570, 570), nodename="MixBlue", blendtype="MULTIPLY", hide=True)
    CreateNode("ShaderNodeRGB", (-1300, 800), nodename="RedColor")
    CreateNode("ShaderNodeRGB", (-1100, 800), nodename="GreenColor")
    CreateNode("ShaderNodeRGB", (-900, 800), nodename="BlueColor")
    nodes["Albedo"].location = (-1300, 600)
    if "Specular" in nodes:
        nodes["Specular Add"].location = (-700, 300)

    LinkNodesInARow( (FROM("Albedo", "Color"), TO("MixRed", "Color1")), (FROM("Color Mask", "Color"), TO("SeparateMSK", "Image")),
                     (FROM("SeparateMSK", "R"), TO("MixRed", "Fac")), (FROM("SeparateMSK", "G"), TO("MixGreen", "Fac")), (FROM("SeparateMSK", "B"), TO("MixBlue", "Fac")),
                     (FROM("MixRed", "Color"), TO("MixGreen", "Color1")), (FROM("MixGreen", "Color"), TO("MixBlue", "Color1")),
                     (FROM("RedColor", "Color"), TO("MixRed", "Color2")), (FROM("GreenColor", "Color"), TO("MixGreen", "Color2")),
                     (FROM("BlueColor", "Color"), TO("MixBlue", "Color2")), (FROM("MixBlue", "Color"), TO("AO_Mult_Albedo", "Color1")) )
    resetColors()
    CheckAndAddToNodesList("Color Mask")

def PlaceMetalSmoothness():
    PlaceBase()
    CreateNode("ShaderNodeTexImage", (-700, 0), nodename="Metal Smoothness", image=PBR_Panel.MATERIALS['CURRENT'].images["Metal Smoothness"])
    CreateNode("ShaderNodeMath", (-360, 0), nodename="Metallic Add", operation="ADD", hide=True)
    CreateNode("ShaderNodeInvert", (-360, -50), nodename="Invert", hide=True)
    CreateNode("ShaderNodeMath", (-360, -100), nodename="Roughness Add", operation="ADD", hide=True)
    LinkNodesInARow( (FROM("Metal Smoothness", "Alpha"), TO("Invert", "Color")), (FROM("Invert", "Color"), TO("Roughness Add", "Value")),
                     (FROM("Roughness Add", "Value"), TO("Principled BSDF", "Roughness")), (FROM("Metal Smoothness", "Color"), TO("Metallic Add", "Value")),
                     (FROM("Metallic Add", "Value"), TO("Principled BSDF", "Metallic")) )
    CheckAndAddToNodesList("Metal Smoothness")

def PlaceMetalRoughness():
    PlaceBase()
    if PBR_Panel.MATERIALS['CURRENT'].found["Metal"]:
        CreateNode("ShaderNodeTexImage", (-700, 0), nodename="Metal", image=PBR_Panel.MATERIALS['CURRENT'].images["Metal"])
        CreateNode("ShaderNodeMath", (-360, 0), nodename="Metallic Add", operation="ADD", hide=True)
        LinkNodesInARow( (FROM("Metal", "Color"), TO("Metallic Add", "Value")), (FROM("Metallic Add", "Value"), TO("Principled BSDF", "Metallic")) )
        CheckAndAddToNodesList("Metal")
    if PBR_Panel.MATERIALS['CURRENT'].found["Roughness"]:
        CreateNode("ShaderNodeTexImage", (-1000, -300), nodename="Roughness", image=PBR_Panel.MATERIALS['CURRENT'].images["Roughness"])
        CreateNode("ShaderNodeMath", (-360, -250), nodename="Roughness Add", operation="ADD", hide=True)
        LinkNodesInARow( (FROM("Roughness", "Color"), TO("Roughness Add", "Value")), (FROM("Roughness Add", "Value"), TO("Principled BSDF", "Roughness")) )
        CheckAndAddToNodesList("Roughness")

def PlaceCoordinates():
    nodes = bpy.context.object.active_material.node_tree.nodes
    CreateNode("ShaderNodeUVMap", (-1900, 600), nodename="UVMap")
    CreateNode("ShaderNodeMapping", (-1700, 600), nodename="Mapping")
    nodes['UVMap'].uv_map = bpy.data.meshes[bpy.context.active_object.name].uv_layers.keys()[0]
    LinkNodes( FROM("UVMap", "UV"), TO("Mapping", "Vector") )
    for texture in PBR_Panel.MATERIALS['CURRENT'].found:
        if PBR_Panel.MATERIALS['CURRENT'].found[texture] and texture in nodes:
            LinkNodes( FROM("Mapping", "Vector"), TO(texture, "Vector") )

def PlaceAutomatic():
    PlaceBase()
    if PBR_Panel.MATERIALS['CURRENT'].found["ORM"]:
        PlaceORMMSK() if PBR_Panel.MATERIALS['CURRENT'].found["Color Mask"] else PlaceORM()
    else:
        if PBR_Panel.MATERIALS['CURRENT'].found["Metal Smoothness"]:
            PlaceMetalSmoothness()
        elif any(texture in PBR_Panel.MATERIALS['CURRENT'].found for texture in ["Metal", "Roughness"]):
            PlaceMetalRoughness()
        PlaceOcclusion()
    if any(PBR_Panel.MATERIALS['CURRENT'].found[texture] for texture in PBR_Panel.MATERIALS['CURRENT'].found):
        PlaceCoordinates()
    resetProps()

def PlaceManual(PipeLineType):
    PBR_Panel.MATERIALS['CURRENT'].softreset()
    PBR_Panel.MATERIALS['CURRENT'].automatic = False
    if PipeLineType == "MetalRoughness":
        PlaceMetalRoughness()
    elif PipeLineType == "MetalSmoothness":
        PlaceMetalSmoothness()
    elif PipeLineType == "ORM":
        PlaceORM()
    elif PipeLineType == "ORM+MSK":
        PlaceORMMSK()
    if not any([PipeLineType == "ORM", PipeLineType == "ORM+MSK"]):
        PlaceOcclusion()
    PlaceCoordinates()
    resetProps()
####################################################################################################
#SOME ADDITIONAL FUNCTIONS
####################################################################################################
def GetMode():
    return f"Mode: {' + '.join(PBR_Panel.MATERIALS['CURRENT'].nodeslist)} ({'Automatic' if PBR_Panel.MATERIALS['CURRENT'].automatic else 'Manual'})"

def CheckAndAddToNodesList(mode):
    if mode not in PBR_Panel.MATERIALS['CURRENT'].nodeslist:
        PBR_Panel.MATERIALS['CURRENT'].nodeslist.append(mode)
####################################################################################################
#CHANGE OPACITY CLASS
####################################################################################################
class OpacityMenu(bpy.types.Operator):
    bl_idname = "pbr.showopacitymenu"
    bl_label = "Opaque"
    bl_description = "Set opacity mode"

    def execute(self, context):
        wm = bpy.context.window_manager
        wm.popup_menu(OpacityMenu.ShowMenu)
        return {"FINISHED"}

    def ShowMenu(self, context):
        layout = self.layout
        layout.operator(OpaqueMode.bl_idname)
        layout.operator(CutoutMode.bl_idname)
        layout.operator(FadeMode.bl_idname)

class OpaqueMode(bpy.types.Operator):
    bl_idname = "pbr.opaque"
    bl_label = "Opaque"
    bl_description = "opaque mode"

    def execute(self, context):
        updateOpacityAdd('CLEAR')
        PBR_Panel.MATERIALS['CURRENT'].opacity_mode = "Opaque"
        bpy.context.object.active_material.use_backface_culling = False
        bpy.context.object.active_material.blend_method = "OPAQUE"
        bpy.context.object.active_material.shadow_method = "OPAQUE"
        return {"FINISHED"}

class CutoutMode(bpy.types.Operator):
    bl_idname = "pbr.cutout"
    bl_label = "Cutout"
    bl_description = "cutout mode"

    def execute(self, context):
        updateOpacityAdd('CLEAR')
        PBR_Panel.MATERIALS['CURRENT'].opacity_mode = "Cutout"
        bpy.context.object.active_material.use_backface_culling = True
        bpy.context.object.active_material.blend_method = "CLIP"
        bpy.context.object.active_material.shadow_method = "CLIP"
        return {"FINISHED"}

class FadeMode(bpy.types.Operator):
    bl_idname = "pbr.fade"
    bl_label = "Fade"
    bl_description = "fade mode"

    def execute(self, context):
        updateOpacityAdd('CREATE')
        PBR_Panel.MATERIALS['CURRENT'].opacity_mode = "Fade"
        bpy.context.object.active_material.use_backface_culling = True
        bpy.context.object.active_material.blend_method = "BLEND"
        bpy.context.object.active_material.shadow_method = "HASHED"
        return {"FINISHED"}

def updateOpacityAdd(mode):
    nodes = bpy.context.object.active_material.node_tree.nodes
    if mode == 'CLEAR':
        if 'Opacity Add' in nodes:
            from_node_name = nodes['Opacity Add'].inputs['Value'].links[0].from_node.name
            from_socket_name = nodes['Opacity Add'].inputs['Value'].links[0].from_socket.name
            to_node_name = nodes['Opacity Add'].outputs['Value'].links[0].to_node.name
            to_socket_name = nodes['Opacity Add'].outputs['Value'].links[0].to_socket.name
            LinkNodes( FROM(from_node_name, from_socket_name), TO(to_node_name, to_socket_name) )
            nodes.remove(nodes['Opacity Add'])
        return
    elif mode == 'CREATE':
        node_name = nodes['Principled BSDF'].inputs['Alpha'].links[0].from_node.name
        if node_name == 'Albedo':
            socket_name = 'Alpha'
            if 'ORM' in PBR_Panel.MATERIALS['CURRENT'].nodeslist:
                location = (-960, 520)
            else:
                location = (-360, 200)
        elif node_name == 'Opacity':
            socket_name = 'Color'
            location = (-700, -560)
        CreateNode("ShaderNodeMath", location, nodename="Opacity Add", operation="ADD", defaultinput=(1, 0), hide=True)
        print(node_name, socket_name) 
        LinkNodesInARow( (FROM(node_name, socket_name), TO("Opacity Add", "Value")), (FROM("Opacity Add", "Value"), TO("Principled BSDF", "Alpha")) )
    return
####################################################################################################
#CHANGE PIPELINE CLASS
####################################################################################################
class PipelineMenu(bpy.types.Operator):
    bl_idname = "pbr.pipelinemenu"
    bl_label = "Change Pipeline"
    bl_description = "Set pipeline (ORM/MetalSmoothness/etc.)"

    def execute(self, context):
        wm = bpy.context.window_manager
        wm.popup_menu(PipelineMenu.ShowMenu, title="Found pipelines")
        return {"FINISHED"}

    def ShowMenu(self, context):
        layout = self.layout
        if PBR_Panel.MATERIALS['CURRENT'].found["ORM"]:
            layout.operator(ORMTexturer.bl_idname, text = "ORM")
            if PBR_Panel.MATERIALS['CURRENT'].found["Color Mask"]:
                layout.operator(ORMMSKTexturer.bl_idname, text = "ORM+MSK")
        if PBR_Panel.MATERIALS['CURRENT'].found["Metal Smoothness"]:
            layout.operator(MetalSmoothnessTexturer.bl_idname, text = "Metal Smoothness")
        if PBR_Panel.MATERIALS['CURRENT'].found["Metal"] or PBR_Panel.MATERIALS['CURRENT'].found["Roughness"]:
            if PBR_Panel.MATERIALS['CURRENT'].found["Metal"] and PBR_Panel.MATERIALS['CURRENT'].found["Roughness"]:
                text = "Metal+Roughness"
            elif PBR_Panel.MATERIALS['CURRENT'].found["Metal"]:
                text = "Metal"
            elif PBR_Panel.MATERIALS['CURRENT'].found["Roughness"]:
                text = "Roughness"
            layout.operator(MetalRoughnessTexturer.bl_idname, text = text)
        if not any(texture in PBR_Panel.MATERIALS['CURRENT'].found for texture in ["ORM", "Metal Smoothness", "Metal", "Roughness"]):
            layout.label(text = "No options")

class MetalRoughnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metalroughness"
    bl_label = "MetalRoughness"
    bl_description = "Create Metal/Roughness Pipeline"

    def execute(self, context):
        PlaceManual("MetalRoughness")
        return {"FINISHED"}

class MetalSmoothnessTexturer(bpy.types.Operator):
    bl_idname = "pbr.metsm"
    bl_label = "Metal Sm."
    bl_description = "Create Metal Smothness Pipeline"

    def execute(self, context):
        PlaceManual("MetalSmoothness")
        return {"FINISHED"}

class ORMTexturer(bpy.types.Operator):
    bl_idname = "pbr.orm"
    bl_label = "ORM"
    bl_description = "Create ORM Pipeline"

    def execute(self, context):
        PlaceManual("ORM")
        return {"FINISHED"}

class ORMMSKTexturer(bpy.types.Operator):
    bl_idname = "pbr.ormmsk"
    bl_label = "ORM+MSK"
    bl_description = "Create ORM+MSK Pipeline"

    def execute(self, context):
        PlaceManual("ORM+MSK")
        return {"FINISHED"}
####################################################################################################
#SUBPANELS CLASSES
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
    def poll(self, context):
        if bpy.context.selected_objects == []:
            return False
        return PBR_Panel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material != None

    def draw(self, context):
        layout = self.layout
        for texture in PBR_Panel.MATERIALS['CURRENT'].found:
            if PBR_Panel.MATERIALS['CURRENT'].found[texture]:
                row = layout.row()
                row.label(text = f"{texture}:")
                sub = row.row()
                sub.label(text = f"{PBR_Panel.MATERIALS['CURRENT'].images[texture].name}")

class UVMapPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_UV"
    bl_space_type = "PROPERTIES"
    bl_label = "UV"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(self, context):
        if bpy.context.selected_objects == []:
            return False
        return PBR_Panel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material != None and len(bpy.data.meshes[bpy.context.active_object.name].uv_layers.keys())>1

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
    def poll(self, context):
        if bpy.context.selected_objects == []:
            return False
        return PBR_Panel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material != None

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if PBR_Panel.MATERIALS['CURRENT'].nodeslist == []:
            row.label(text = "Mode: None")
        else:
            row.label(text = GetMode())
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
    def poll(self, context):
        if bpy.context.selected_objects == []:
            return False
        return PBR_Panel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material != None

    def draw(self, context):
        MaterialProps = bpy.context.active_object.active_material.props
        layout = self.layout
        if not PBR_Panel.MATERIALS['CURRENT'].found["Albedo"]:
            row = layout.row()
            row.prop(MaterialProps, "AlbedoColor")
        if "Normal Map" in PBR_Panel.MATERIALS['CURRENT'].nodeslist:
            row = layout.row(align = False)
            row.scale_x = 2.5
            row.prop(MaterialProps, "NormaMaplStrength")
            sub = row.row(align = False)
            sub.scale_x = 0.6
            sub.prop(MaterialProps, "NormalMapInvertorEnabled")
        TexturePropsPanel.ShowProp(context, layout, ["Metal", "ORM", "Metal Smoothness"], ["MetallicAdd"])
        TexturePropsPanel.ShowProp(context, layout, ["Roughness", "ORM", "Metal Smoothness"], ["RoughnessAdd"])
        TexturePropsPanel.ShowProp(context, layout, ["Emission"], ["EmissionMult"])
        TexturePropsPanel.ShowProp(context, layout, ["ORM", "Occlusion"], ["AO_Strength"])
        TexturePropsPanel.ShowProp(context, layout, ["Specular"], ["SpecularAdd"])
        TexturePropsPanel.ShowProp(context, layout, ["Color Mask"], ["MixR", "MixG", "MixB"], header="Color mask settings:")

    def ShowProp(context, layout, textures, properties, header=""):
        MaterialProps = bpy.context.active_object.active_material.props
        if any(texture in PBR_Panel.MATERIALS['CURRENT'].nodeslist for texture in textures):
            if header != "":
                row = layout.row()
                row.label(text = header)
            for property in properties:
                row = layout.row()
                row.prop(MaterialProps, property)

class TextureCoordinatesPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_TexturesCoordinates"
    bl_space_type = "PROPERTIES"
    bl_label = "Texture Coordinates"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        if bpy.context.selected_objects == []:
            return False
        return PBR_Panel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material != None and "Mapping" in bpy.context.object.active_material.node_tree.nodes

    def draw(self, context):
        MaterialProps = bpy.context.active_object.active_material.props
        layout = self.layout
        for property in ["Location", "Rotation", "Scale"]:
            row = layout.row()
            row.prop(MaterialProps, property)

class OpacityPanel(bpy.types.Panel):
    bl_parent_id = "PBR_PT_Core"
    bl_idname = "PBR_PT_opacity_mode"
    bl_space_type = "PROPERTIES"
    bl_label = "Opacity Settings"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"HIDE_HEADER"}

    @classmethod
    def poll(self, context):
        if 'CURRENT' in PBR_Panel.MATERIALS:
            return (PBR_Panel.MATERIALS['CURRENT'].opacity_from_albedo or PBR_Panel.MATERIALS['CURRENT'].found["Opacity"]) and \
            PBR_Panel.MATERIALS['CURRENT'].finished and bpy.context.active_object.active_material != None and bpy.context.selected_objects != []
        return False

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Opacity Mode:")
        row.operator(OpacityMenu.bl_idname, text=PBR_Panel.MATERIALS['CURRENT'].opacity_mode)
        MaterialProps = bpy.context.active_object.active_material.props
        if PBR_Panel.MATERIALS['CURRENT'].opacity_mode == "Cutout":
            row = layout.row()
            row.prop(context.active_object.active_material.props, "AlphaTreshold")
        if PBR_Panel.MATERIALS['CURRENT'].opacity_mode == "Fade":
            row = layout.row()
            row.prop(MaterialProps, "AlphaMode")
            row = layout.row()
            row.prop(MaterialProps, "OpacityAdd")
####################################################################################################
#TEXTURE GETTER CLASS
####################################################################################################
class GetTextureOperator(bpy.types.Operator):
    bl_idname = "textures.get"
    bl_label = "Assign Textures"
    bl_description = "Assign files with textures using choosen name pattern"

    current_file = None

    def execute(self, context):
        ClearImages()
        PBR_Panel.MATERIALS['CURRENT'].reset()
        path = bpy.context.active_object.active_material.props.conf_path
        filenames = next(os.walk(path), (None, None, []))[2]
        for file in filenames:
            GetTextureOperator.current_file = file
            for texture in TEXTURES:
                colored = any(texture == colored for colored in ["Albedo", "Emission", "Specular", "Occlusion"])
                if not PBR_Panel.MATERIALS['CURRENT'].found[texture]:
                    if GetTextureOperator.getTexture(texture, Colored = colored):
                        continue
        PBR_Panel.MATERIALS['CURRENT'].finished = True
        PlaceAutomatic()
        return {"FINISHED"}

    def getTexture(texture, Colored = False):
        file = GetTextureOperator.current_file
        if len(file.split(".")) >= 3:
            return False
        name = file.lower().split(".")[0]
        if texture != "Albedo":
            checkmask = TEXTURES_MASK.copy()
            checkmask.pop(texture)
            if any(name.endswith(checkmask[texture]) for texture in checkmask):
                return False
        pattern = bpy.context.active_object.active_material.props.texture_pattern.lower().split("-")
        if len(pattern)>1:
            pattern, skip = pattern[0], pattern[1]
        else:
            pattern, skip = pattern[0], None
        if skip != None and skip in name:
            return False
        if name.endswith(TEXTURES_MASK[texture]) and pattern in name:
            if file in bpy.data.images:
                image = bpy.data.images[file]
            else:
                image = bpy.data.images.load(filepath = os.path.join(bpy.context.active_object.active_material.props.conf_path,file))
            if not Colored:
                image.colorspace_settings.name = "Non-Color"
            PBR_Panel.MATERIALS['CURRENT'].found[texture], PBR_Panel.MATERIALS['CURRENT'].images[texture] = True, image
        return True
####################################################################################################
#MAIN PANEL CLASS
####################################################################################################
class PBR_Panel(bpy.types.Panel):
    bl_label = "Easy PBR Hook"
    bl_idname = "PBR_PT_Core"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    current_path = ""
    current_pattern = ""
    MATERIALS = {}

    @classmethod
    def poll(self, context):
        return bpy.context.active_object.active_material != None

    def draw(self, context):
        MaterialProps = bpy.context.active_object.active_material.props
        PBR_Panel.current_path = MaterialProps.conf_path
        PBR_Panel.current_pattern = MaterialProps.texture_pattern
        layout = self.layout
        if PBR_Panel.BadState(layout):
            return
        PBR_Panel.UpdateMaterial()
        row = layout.row()
        row.prop(MaterialProps, "conf_path")
        row = layout.row()
        row.prop(MaterialProps, "texture_pattern")
        PBR_Panel.AssignTextures(layout)

    def UpdateMaterial():
        material_name = bpy.context.selected_objects[0].active_material.name
        if 'CURRENT' not in PBR_Panel.MATERIALS:
            Material(material_name)
        elif PBR_Panel.MATERIALS['CURRENT'].name != material_name:
            if material_name not in PBR_Panel.MATERIALS:
                Material(material_name)
            else:
                PBR_Panel.MATERIALS['CURRENT'] = PBR_Panel.MATERIALS[material_name]

    def BadState(layout):
        if bpy.context.selected_objects==[]:
            row = layout.row()
            row.label(text = "No object")
            return True
        if bpy.context.selected_objects[0].active_material == None:
            row = layout.row()
            row.label(text = "No material")
            PBR_Panel.MATERIALS['CURRENT'].finished = False
            return True
        return False

    def AssignTextures(layout):
        row = layout.row()
        text = "Reassign textures" if PBR_Panel.MATERIALS['CURRENT'].finished else "Assign textures"
        row.operator(GetTextureOperator.bl_idname, text=text)
####################################################################################################
#CLASSES LIST, REGISTER AND RUN
####################################################################################################
modules = [PBR_Panel, UVMapProp, MaterialProps, GetTextureOperator, PipelineMenu,
           ORMTexturer, MetalSmoothnessTexturer, MetalRoughnessTexturer, ORMMSKTexturer,
           FadeMode, OpaqueMode, CutoutMode, OpacityMenu, 
           UVMapPanel, TextureListPanel, TextureModePanel, TexturePropsPanel, TextureCoordinatesPanel, OpacityPanel]

def register():
    for module in modules:
        bpy.utils.register_class(module)

def unregister():
    for module in modules:
        bpy.utils.unregister_class(module)

if __name__ == "__main__":
    register()
