## Easy PBR Hook found textures but some textures are pink-colored
This situation happens if you have "corrupted" images in your blendfile. When you click on "Assign Textures" button or "Reload Material" button Easy PBR Hook not only looks through your folder but through your blendfile too. If plugin found propper texture in your blendfile this image will be used in your material. If this image is corrupted you will get fancy pink colored mesh. 

In blendfile Blender stores not an image but just a link (path) to it. Corrupted file means blendfile contains link to image with invalid path. It happens if someone forgot to pack texture to blendfile. If you want blender to save image you need to pack it using file->external data->pack all into .blend. 

To fix this problem you need to delete this image from blendfile. Now try to reload material again

## I set up everything but Easy PBR Hook can't find my textures
In this case you need to check your naming convention table and compare it with your textures namings. If there are some differences you just need to append new keys to your naming convention table and global/local update it. Visit Documentation for more details.

If you still have some problems you need to contact me. In your email you need to describe your problem and include zip/rar-archive with your textures. I will help you and if there are some bugs in script I'll fix them.

## I don't see Easy PBR Hook panel in Material tab
First of all check if it's installed and activated. Easy PBR Hook panel is shown if: 1) you have a selected mesh and 2) you have material instance. So all you need to do is just click on mesh and create new material instance if you don't have one.