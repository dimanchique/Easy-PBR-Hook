import bpy

__all__ = ['create_node', 'link_nodes', 'link_nodes_in_a_row', 'FROM', 'TO', 'create_sockets']


def create_node(node_type,
                loc,
                node_name="",
                blend_type="",
                operation="",
                nodegroup=None,
                image=None,
                hide=False,
                default_input=None,
                nodetree="default"):
    nodes = bpy.context.object.active_material.node_tree.nodes if nodetree == "default" else nodetree.nodes
    new_node = nodes.new(node_type)
    new_node.location = loc
    if node_name:
        new_node.label = new_node.name = node_name
    if blend_type:
        new_node.blend_type = blend_type
    if operation:
        new_node.operation = operation
    if nodegroup:
        new_node.node_tree = bpy.data.node_groups[nodegroup]
    if image:
        new_node.image = image
    if default_input:
        new_node.inputs[default_input[0]].default_value = default_input[1]
    new_node.hide = hide


def link_nodes(from_socket, to_socket, nodetree="default"):
    node_tree = bpy.context.object.active_material.node_tree if nodetree == "default" else nodetree
    node_tree.links.new(node_tree.nodes[from_socket[0]].outputs[from_socket[1]],
                        node_tree.nodes[to_socket[0]].inputs[to_socket[1]])


def link_nodes_in_a_row(*routes, nodetree="default"):
    [link_nodes((route[0][0], route[0][1]), (route[1][0], route[1][1]), nodetree) for route in routes]


def FROM(name, socket):
    return [name, socket]


def TO(name, socket):
    return [name, socket]


def create_sockets(node, *sockets, socket=""):
    node_sockets = node.inputs if socket == "INPUT" else node.outputs
    [node_sockets.new(socket_type, socket) for socket_type, socket in sockets]
