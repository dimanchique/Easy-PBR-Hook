# Easy PBR Hook
Easy PBR Hook add-on is a really powerful tool for gamedev guys!<br />
This tool can save a lot of time you spending to configure you material!<br />
# Common Features
- Automatic search textures in the specified folder
- Special search settings: you can type **keyword** to find specific texture in folder, or you can use minus sign to set **stop word** and ignore some textures in folder, and even both!
- Automatic creating of nodes for found textures (not for all at the same time! We have a priority system: ORM+Color Mask -> ORM -> Metal Smoothness -> Metal/Roughness)
- Creating not only texture nodes, but control nodes too! Normal Map Strength, Metallic Add, Ambient Occlusion Multiply and a lot of other stuff!
- Control every parametr of you material in one place! For every property (as written above) we creating a control tool (switch/slider/etc.) and all of this controls stores in one sub panel called **Texture Properties**
# Guide
- **Installation**<br />
  Install script to Blender. Go to Edit->Preferences->Add-ons->Install...<br />
  Choose Easy_PBR_Hook_x_x_x.py, click "Install Add-on" and enable it.<br />
  Now, in your Material Properties you have Easy PBR Hook Panel.<br />
- **Usage**<br />
  Go to the material tab of your model, select a material you want to set up. Scroll down to Easy PBR Hook section. 

  Paste or select a path to the texture folder.
  
  If there are multiple texture sets in said folder you can use the Keyword field to determine which texture set will be used. 
  
  Click Assign textures button. You're done.
  
  If your textures are as messy as mine you could have MetalSmoothness, OcclusionRoughnessMetallic, Metallic and Roughness maps in the same folder.
  If that's the case Easy PBR Hook will choose one of those and create a full set up. If you want to use another Pipeline you can do so via 'Change Pipeline' button. 

  Use Texture Properties and Texture Coordinates drop-downs to further set up the look of your material.
