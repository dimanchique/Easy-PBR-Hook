![](https://assets.superhivemarket.com/store/product/174355/image/1375158afd05e29fc6ed00aa25e89cd7.png)
![](https://assets.superhivemarket.com/store/productimage/270226/image/e24e61bb8acc91aa745e429130e63459.png)
# What is Easy PBR Hook?
Easy PBR Hook is an add-on to set up your PBR materials in Blender in 1 click. It looks for textures within a specified folder using user-defined keywords and connects found textures to the Principled BSDF shader appropriately. 

![](https://assets.superhivemarket.com/cache/7292c0a972fc7a30cdbd663fb4852840.gif)

### Youtube Demo: [LINK](https://youtu.be/dqX5fHjpWTA) <br>
### Details: [LINK](docs/DETAILS.md) <br>
### FAQ: [LINK](docs/FAQ.md) <br>

## Main Features
- Automatically finds textures within a specified folder
- Automatically recognizes textures using the fully customizable naming convention table. For example, textures with names ending with "basecolor", "base_color", "bc", "color", "albedo", etc. will be determined as a Base Color texture. You can customize the naming convention for current project only (local update), or for all of your projects (global update). You can also export/import your naming convention table and even go back to the default at any time

![](https://assets.superhivemarket.com/cache/ca1d7f129c022df1a3277804bb2bd71f.png)

- Customizable search: you can use a keyword to narrow down the search if there are several texture map sets in one folder. You can also use minus sign to exclude a word from search. Multiple excluding support

![](https://assets.superhivemarket.com/cache/7c13d639b1ef36f398a6f7d764ea1a7a.png)

*in this case "old" textures will be skipped*

- Automatic setup of nodes for found textures. For example, a smoothness map will be put through an Invert node and connected to the Roughness input of the Principled BSDF shader node
- If you have several texture sets using different packing pipelines in the same folder our add-on will use only one in following priority: ORM+Color Mask -> ORM -> MetallicSmoothness -> Standard Unpacked while still having an option to manually switch between them

![](https://assets.superhivemarket.com/cache/061b65699d4ae1a52c94f1f80590f784.gif)

- Not only creates and connects texture nodes, but also creates control switches and sliders in the material tab allowing you to never even bother opening the shader editor to invert your normals or increase roughness etc.

![](https://assets.superhivemarket.com/cache/cc01fcbbf90ce5cad1cf9df2be16615b.gif)

> **_NOTE:_** You can use "Simplify" checkbox to disable creating math nodes. It will take effect after reloading your material

![](https://assets.superhivemarket.com/cache/2342dcfe12299520400eef3744c9769d.gif)

- Each material remembers the texture address, the keywords used and parameters

![](https://assets.superhivemarket.com/cache/d340f214c89ccfd00396aaa2be2c4f30.gif)

- UDIM textures support

### List of recognized textures
- Albedo
- Metal Smoothness
- Metal
- Roughness
- ORM
- Color Mask
- Normal Map
- Emission
- Specular
- Occlusion
- Displacement
- Opacity
- Detail Map
- Detail Mask

### Info:
For questions, support, bug report and funny memes: [e-mail](mailto:blender.dmitriy@gmail.com)