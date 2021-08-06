# Easy PBR Hook
Easy PBR Hook add-on is a really powerful tool for gamedev guys! This tool can save a lot of time you spending to configure you material!<br />
# Common Features
- **Supported textures**: Base Color, Metal, Roughness, Metal Smoothness, ORM, Opacity, Specular, Color Mask, Displacement, and Occlusion. 
- We have a lot of **keywords for every type of texture** to catch 'em all!
- **Automatic search** textures in the specified folder
- Special search settings: you can type **keyword** to find specific texture in folder, or you can use minus sign to set **stop word** and ignore textures containing this word, **and even both**!
- **Automatic creating** of nodes for found textures (not for all at the same time! We have a priority system: ORM+Color Mask -> ORM -> Metal Smoothness -> Metal/Roughness).
- Full configuration of your material is **descripted in one line**.
- Creating not only texture nodes, but **control nodes too**! Normal Map Strength, Metallic Add, Ambient Occlusion Multiply and a lot of other stuff!
- **Control every parameter** of you material in one place! For every property (as written above) we creating a control tool (switch/slider/buton) and each control stores in one sub panel called **Texture Properties**
- If you have a multiple materials, so **every material has it's own properties and textures!** You have something like MEMORY to create as much materials as you want!
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
