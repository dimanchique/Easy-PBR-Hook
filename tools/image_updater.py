import bpy
import os
from .global_tools import Tools

__all__ = ['UpdateImagesOperator']


class UpdateImagesOperator(bpy.types.Operator):
    bl_idname = "pbr.image_updater_op"
    bl_label = "Update images"
    bl_description = "Update images for current material"

    @staticmethod
    def execute(self, context):
        nodes = bpy.context.object.active_material.node_tree.nodes
        image_warnings = 0
        file_warnings = 0
        for node in nodes:
            if hasattr(nodes[node.name], 'image'):
                if nodes[node.name].image is not None:
                    image_name = nodes[node.name].image.name
                    path = os.path.join(bpy.context.active_object.active_material.props.textures_path, image_name)
                    if os.path.isfile(path):
                        bpy.data.images[image_name].reload()
                    else:
                        file_warnings += 1
                else:
                    image_warnings += 1

        self.get_report(image_warnings, file_warnings)
        return {"FINISHED"}

    def get_report(self, image_warnings, file_warnings):
        if any([image_warnings, file_warnings]):
            file_warnings = '' if file_warnings == 0 else f'Missing files ({file_warnings})'
            image_warnings = '' if image_warnings == 0 else f'Missing image in nodes ({image_warnings})'
            self.report({'WARNING'}, 'Image update finished with errors. ' + file_warnings + ' ' + image_warnings)
        else:
            self.report({'INFO'}, Tools.IMAGE_UPDATE)


def register():
    bpy.utils.register_class(UpdateImagesOperator)


def unregister():
    bpy.utils.unregister_class(UpdateImagesOperator)
