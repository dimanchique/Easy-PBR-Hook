# Easy PBR Hook
Easy PBR Hook is an add-on to set up your PBR materials in Blender in 1 click. It looks for textures within a specified folder using user-defined keywords and connects found textures to the Principled BSDF shader appropriately. It also supports game-dev packed texture maps like MetallicSmoothness for Unity and OcclusionRoughnessMetallic for Unreal Engine. It can filter through messy folders containing multiple texture sets finding the one you need for the specific material.
# Main Features
- **Automatically finds** textures within a specified folder
- **Automatically recognizes** textures using the naming. For example textures with names ending with "basecolor", "base_color", "bc", "color", "albedo", "albedotransparency", "albedo_transparency", "diffuse", "diffusemap", "diffuse_map", "alb" will be determined as a Base Color texture.
- **Customizable search**: you can use a **keyword** to narrow down the search if there are several texture map sets in one folder. You can also use minus sign to exclude a word from search.
- **Automatic setup** of nodes for found textures. A smoothness map will be put through an Invert node and connected to the Roughness input of the Principled BSDF shader node.
- If your texture folder is as messy as ours and you have several texture sets using different packing pipelines in the same folder our plug-in will use only one in following priority: *ORM+Color Mask -> ORM -> MetallicSmoothness -> Standard Unpacked* while still having an option to manually switch between them.
- Not only creates and connects texture nodes, but also creates control switches and sliders in the material tab allowing you to never even bother opening the shader editor to invert your normals or increase roughness etc. 
- Each material remembers the texture address and the keywords used. 
- **Supported textures**: Base Color, Metal, Roughness, MetallicSmoothness, ORM, Opacity, Specular, Color Mask, Displacement, Occlusion, Emission.
# Guide
- **Installation**<br />
  Install script to Blender. Go to Edit->Preferences->Add-ons->Install...<br />
  Choose Easy_PBR_Hook_x_x_x.py, click "Install Add-on" and enable it.<br />
  Now, in your Material Properties you have Easy PBR Hook Panel.<br />
- **Usage**<br />
  Go to the material tab of your model, select a material you want to set up. Scroll down to Easy PBR Hook section. You're in the game now!<br />
  Paste or select a path to the texture folder. If there are multiple texture sets in said folder you can use the Keyword field to determine which texture set will be used. Click Assign textures button. You're done.<br/>
  If your textures are as messy as mine you could have MetalSmoothness, OcclusionRoughnessMetallic, Metallic and Roughness maps in the same folder. If that's the case Easy PBR Hook will choose one of those and create a full set up. If you want to use another Pipeline you can do so via 'Change Pipeline' button.<br />
  Use Texture Properties and Texture Coordinates drop-downs to further set up the look of your material.
- **Recognized texture namings**<br />
**Albedo:** *basecolor, base_color, bc, color, albedo, albedotransparency, albedo_transparency, diffuse, diffusemap, diffuse_map, alb* <br />
**Metal Smoothness:** *metsm, met_sm, metal_smoothness, metalic_smoothness, metalsmoothness, metallicsmoothness, metal_smooth, metalsmooth, metsmooth* <br />
**Metal:** *met, metal, \_m, metall, metallic* <br />
**Roughness:** *\_r, rough, roughness* <br />
**ORM:** *\_orm, occlusionroughnessmetallic* <br />
**Color Mask:** *\_m, msk, colormask, color_mask, \_mask* <br />
**Normal Map:** *normal, nm, \_n, normal_map, normalmap, normaldx, normal_dx, nrm* <br />
**Emission:** *\_e, emis, emiss, emission* <br />
**Specular:** *\_s, specular, spec* <br />
**Occlusion:** *occlusion, \_ao, ambientocclusion* <br />
**Displacement:** *displacement, height, hightmap* <br />
**Opacity:** *opacity transparency* <br />
**Detail Map:** *detailnrm, detail_nrm, detail, detailmap, detail_map, detail_n, detailn* <br />
**Detail Mask:** *detailmsk, detail_msk, detailmask, detail_mask, detmsk, det_msk, detmask, det_mask* <br />
