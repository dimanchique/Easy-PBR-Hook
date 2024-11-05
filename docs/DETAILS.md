## How to install:
Launch Blender, go to Edit->Preferences->Add-ons->Install..., choose Easy PBR Hook zip-archive and activate plugin.

> In case you don't see Easy PBR Hook in list of available add-ons, check if Community add-ons enabled and you're in Material section

![](https://markets-rails.s3.amazonaws.com/cache/1db27bb8f338720b1487a36d4a42c87b.png)

Now, in your Material Properties you have Easy PBR Hook Panel.

![](https://markets-rails.s3.amazonaws.com/cache/db4f35c5a977dc156de6fb08f4f9f569.png)

## Basic usage:
Go to the material tab of your model, select/create a material you want to set up. Paste or select a path to the texture folder.

> If you have multiple materials for one mesh and textures a stored in one folder you can use "Set Shared Path" button. Selected path will be copied to other materials of this mesh 

If there are multiple texture sets in said folder you can use the Keyword field to determine which texture set will be used.

> **_NOTE:_** Easy PBR Hook is looking through folder file to file (not sorted) and if one texture was found, all other textures of this type will be ignored

> **_NOTE:_** Assign Textures button is unavailable if Path field is empty but Keyword field is advanced feature, and you can leave this field empty if you don't want to use it

## How to use keyword:
Imagine we have a folder with these textures:

![](https://markets-rails.s3.amazonaws.com/cache/8026ceb0c7fa1ecd8730becfece473d8.png)

In this case, Easy PBR Hook can make some mistakes. To make it work properly you can enter keywords that will help PBR Hook find exact textures.

> **_NOTE:_** This field is non-case sensitive

If you want to ignore some files you can add '-' in the beginning of the keyword. You can use as much ignore keywords as you want.

> **_NOTE:_** You can add whitespace between keywords. blabla -abc and blabla-abc are the same

Possible options listed below

| keyword       | result                                                                         | description                                                                                                                                                                                                                                  |
|---------------|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| (empty)       | T_AirConditioner_new_BC;<br>T_AirConditioner_new_ORM;<br>T_AirConditioner_N;   | The first file PBR Hook sees is T_AirConditioner_N so it was loaded,<br>Next texture is T_AirConditioner_new_BC,<br>The last one is T_AirConditioner_new_ORM.<br>Other textures has the same type as founded before so they will be ignored. |
| -new          | T_AirConditioningPipe_BC;<br>T_AirConditioningPipe_ORM;<br>T_AirConditioner_N; | Again, the first file PBR Hook sees is T_AirConditioner_N,<br>Next texture is T_AirConditioningPipe_BC,<br>The last one is T_AirConditioningPipe_ORM.<br>Textures with "new" were ignored.                                                   |
| -new<br>-pipe | T_AirConditioning_BC;<br>T_AirConditioning_ORM;<br>T_AirConditioner_N;         | Now we have only T_AirConditioning pack of textures.<br>Textures with "new" and "pipe" were ignored.                                                                                                                                         |

In case your Material name matches texture keyword you can use "Use Material name as Keyword" checkbox. Easy PBR Hook will remember previous key word so when you will uncheck it you will see previous keyword in keyword field.

> **_NOTE:_** It will be empty if it was empty before

## How to use texture naming conventions:
We used our experience to collect the most popular naming conventions for every type of supported textures. If you use another style, or you downloaded/bought a pack of textures with another naming convention we created a tool to easy update naming convention table.

Go to "Texture naming convention" and you will see this window:

![](https://markets-rails.s3.amazonaws.com/cache/4f49b7bdb1de88447e56fdc93f9add07.png)

There's a list of supported naming conventions you can modify as you wish. You can delete everything and put preferred suffixes into it, or you can just append some new words.

> **_NOTE:_** You must separate words by comma, otherwise it can cause unexpected behaviour

When you're done you need to set "Update" mode.

You have two options here:

1. "_Local_" means you update naming convention table for current project only. When you will start new project, you will see default naming convention table.
2. "_Global_" means you overwrite a file containing a naming convention table Easy PBR Hook uses. Next time you'll start a project, texture naming convention table will contain your new conventions.

> **_NOTE:_** "_Global_" update calls "_Local_" update first automatically

Also, you have an ability to export/import your naming convention table and even go back to defaults.

When you want to Export it, you need to click "Export" button and select a folder and a filename for export. When you click "Ok" there will be a file "your_filename".json that contains all of your _**Local**_ naming convention.

> **_NOTE:_** Don't forget to update your table before exporting it

Import workflow is the same. You need to click "Import" button and select a .json file in a folder. After clicking "Ok" you will see updated naming convention table (if you chose a proper file). Import function updates your _**Local**_ naming convention.

> **_NOTE:_** Select invalid .json file may cause errors; Selecting non-json file will cause warning message

"_Restoring Defaults_" is a wrap on Import function so it also updates your Local naming convention.

## Assigning textures and Working with Easy PBR Hook:
When you set up Path field (and Keyword field if you need to) Assign Textures button is available. This button makes all magic we worked for. Also, you will see "Simplify" checkbox. Checked state means you don't want to tweak material parameters using math nodes.

> **_NOTE:_** If you will change Path or Keyword field your material will be reset. In this case you will need to click "Assign Textures" button and setup you material again

Now you can see little difference in design of the Easy PBR Hook panel so we will discuss this changes below:

- "_Reload Material_" button causes rebuilding of your material with same behavior as when you press "Assign Textures" button but there's a difference: it doesn't load image if it's already in a blendfile
- "_Update Images_" button causes only updating of already existing images. It's really helpful if all you need is just replace old textures with a new

> **_NOTE:_** New images must have the same name as old

- "_Mode_" section describes the current pipeline. Here you can see which textures are used in your material. At the end of the line you can see "_Automatic_" that means this pipeline was created by Easy PBR Hook
- "_Change Pipeline_" button allows you to change pipeline (if you have not only one). When you click on this button you will see the list of available pipelines Easy PBR Hook found in your textures. Once you changed pipeline you can see "_Mode_" is changed to "_Manual_".
- "_Found Textures_" subpanel is a place where you can see all textures Easy PBR Hook loaded for your material using your Path, Keywords and Naming convention table. It helps you to check if all of your textures are loaded. If not - check your settings and namings.

> **_NOTE:_** If everything seems to be OK, but you still have some problems - notify me using my e-mail, describe your problem and include zip/rar-archive with your textures. I will help you and fix this bug (if it's my fault)

- "_Texture Properties_" subpanel gives you an ability to post-setup your material. Here you'll find an ability to tweak parameters of material depending on found textures.

> **_NOTE:_** This properties won't be shown if you checked "Simplify" material

| Property                                | Shown if                                    | Possible values        |
|-----------------------------------------|---------------------------------------------|------------------------|
| Base Color color-picker                 | Base color NOT in current pipeline          | RGBA                   |
| Normal Strength                         | Normal Map in current pipeline              | 0 to ∞                 |
| Invert Normal                           | Normal Map in current pipeline              | checked/unchecked      |
| Roughness                               | Roughness in current pipeline               | 0 to 2                 |
| Metallic                                | Metallic in current pipeline                | 0 to 2                 |
| Specular                                | Specular in current pipeline                | 0 to 100               |
| Emission                                | Emission in current pipeline                | 0 to ∞                 |
| AO Strength                             | Ambient Occlusion in current pipeline       | 0 to 1                 |
| Opacity                                 | Opacity in current pipeline                 | 0 to 1                 |
| Alpha Threshold                         | Opacity in current pipeline; ? mode enabled | 0 to 1                 |
| Detail Mask Strength                    | Detail Mask in current pipeline             | 0 to 1                 |
| Detail Mask Source                      | Detail Mask in current pipeline             | None/Alpha/Detail Mask |
| Invert Detail Mask                      | Detail Mask in current pipeline             | checked/unchecked      |
| Color Mask Colors<br>(MixR, MixG, MixB) | Color Mask in current pipeline              | RGBA                   |

- "_Texture Coordinates_" subpanel allows you to control coordinates of textures using "_Mapping_" node. This node is connected to every Image Texture node. You can change location, rotation and scale
- "_Detail Map Coordinates_" subpanel is the same as "_Texture Coordinates_" but it's connected to Detail Mask only. 
- "_Opacity Mode_" subpanel is shown if you have Opacity texture map in your pipeline. This subpanel can help you with setup of opacity mode. You have three options here. Default is "_Opaque_", and also you have "_Fade_" and "_Cutout_". Changing "_Opacity mode_" in this subpanel will change Opacity Mode in Principled BSDF settings so you don't need to change it manually. If you set mode to "Cutout" you will get an ability to set the value of "_Alpha Threshold_" parameter. If Opacity Mode is set to "_Fade_" you can switch Alpha Mode between "_Straight_" and "_Channel Packed_" and change value of "_Opacity_" parameter.