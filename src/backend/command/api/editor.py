import os

from flask import Blueprint, jsonify, request, url_for

from command.controller.workspace_editor import WorkspaceEditor
from command.controller.workspace_manager import WorkspaceManager
from utils import exceptions

bp = Blueprint('editor', __name__, url_prefix='/AAZ/Editor')


@bp.route("/Workspaces", methods=("GET", "POST"))
def editor_workspaces():
    if request.method == "POST":
        # create a new workspace
        # the name of workspace is required
        data = request.get_json()
        if not data or not isinstance(data, dict) or 'name' not in data or 'plane' not in data:
            raise exceptions.InvalidAPIUsage("Invalid request body")
        name = data['name']
        plane = data['plane']
        manager = WorkspaceManager.new(name, plane)
        manager.save()
        result = manager.ws.to_primitive()
        result.update({
            'url': url_for('editor.editor_workspace', name=manager.name),
            'folder': manager.folder,
            'updated': os.path.getmtime(manager.path)
        })
    elif request.method == "GET":
        result = []
        for ws in WorkspaceManager.list_workspaces():
            result.append({
                **ws,
                'url': url_for('editor.editor_workspace', name=ws['name']),
            })
    else:
        raise NotImplementedError(request.method)

    return jsonify(result)


@bp.route("/Workspaces/<name>", methods=("GET", "DELETE"))
def editor_workspace(name):
    manager = WorkspaceManager(name)
    if request.method == "GET":
        manager.load()
    elif request.method == "DELETE":
        if manager.delete():
            return '', 200
        else:
            return '', 204  # resource not found
    else:
        raise NotImplementedError()

    result = manager.ws.to_primitive()
    result.update({
        'url': url_for('editor.editor_workspace', name=manager.name),
        'folder': manager.folder,
        'updated': os.path.getmtime(manager.path)
    })
    return jsonify(result)


@bp.route("/Workspace/<name>/Generate", methods=("POST",))
def editor_workspace_generate(name):
    # generate code and command configurations in cli repos and aaz repo
    raise NotImplementedError()


# command tree operations
@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>", methods=("GET", "PATCH", "DELETE"))
def editor_workspace_command_tree_node(name, command_group):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command group not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    node = manager.find_command_tree_node(*root_node_names)
    if not node:
        raise exceptions.ResourceNotFind("Command group not exist")

    if request.method == "GET":
        result = node.to_primitive()
    elif request.method == "PATCH":
        data = request.get_json()
        if 'help' in data:
            manager.update_command_tree_node_help(*root_node_names, help=data['help'])
        if 'stage' in data and node.stage != data['stage']:
            manager.update_command_tree_node_stage(node, data['stage'])
        manager.save()
        result = node.to_primitive()
    elif request.method == "DELETE":
        if len(root_node_names) < 1:
            raise exceptions.InvalidAPIUsage("Not support to delete command tree root")
        if manager.delete_command_tree_node(*root_node_names):
            return '', 200
        else:
            return '', 204  # resource not found
    else:
        raise NotImplementedError()
    return result


@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/Rename", methods=("POST",))
def editor_workspace_command_tree_node_rename(name, command_group):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command group not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    if not manager.find_command_tree_node(*root_node_names):
        raise exceptions.ResourceNotFind("Command group not exist")

    raise NotImplementedError()


@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/Leaves/<command>", methods=("GET", "PUT"))
def editor_workspace_command(name, command_group, command):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    if not manager.find_command_tree_leaf(*root_node_names, command):
        raise exceptions.ResourceNotFind("Command not exist")

    # get the command configuration
    # put update the command configuration
    raise NotImplementedError()


@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/Leaves/<command>/Rename", methods=("POST",))
def editor_workspace_command_rename(name, command_group, command):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    if not manager.find_command_tree_leaf(*root_node_names, command):
        raise exceptions.ResourceNotFind("Command not exist")

    raise NotImplementedError()


# command tree resource operations
@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/AddSwagger", methods=("POST",))
def editor_workspace_swagger_resources(name, command_group):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command group not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    if not manager.find_command_tree_node(*root_node_names):
        raise exceptions.ResourceNotFind("Command group not exist")

    # add new resource
    data = request.get_json()
    if not isinstance(data, dict):
        raise exceptions.InvalidAPIUsage("Invalid request")

    try:
        mod_names = data['module']
        version = data['version']
        resource_ids = data['resources']
    except KeyError:
        raise exceptions.InvalidAPIUsage("Invalid request")

    editor = WorkspaceEditor(manager=manager)

    editor.add_resources_by_swagger(
        mod_names=mod_names,
        version=version,
        resource_ids=resource_ids,
        *root_node_names
    )
    manager.save()
    return "Success"


@bp.route("/Workspace/<name>/Resources", methods=("GET",))
def editor_workspace_resources(name):
    manager = WorkspaceManager(name)
    manager.load()

    raise NotImplementedError()


@bp.route("/Workspace/<name>/Resources/<resource_id>/V/<version>", methods=("GET", "PUT", "DELETE"))
def editor_workspace_resource(name, resource_id, version):
    if request.method == "GET":
        # return the resource configuration
        pass
    elif request.method == "PUT":
        # update the resource configuration
        pass
    elif request.method == "DELETE":
        # delete the resource configuration
        pass
    else:
        raise NotImplementedError(request.method)


@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/Resources/ReloadSwagger", methods=("POST",))
def editor_workspace_resource_reload_swagger(name, command_group):
    # update resource by reloading swagger
    data = request.get_json()
    # data = (resource_id, swagger_version)
    # TODO:
    raise NotImplementedError()


@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/Try", methods=("POST",))
def editor_workspace_try_command_group(name, command_group):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command group not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    if not manager.find_command_tree_node(*root_node_names):
        raise exceptions.ResourceNotFind("Command group not exist")

    # try sub commands by installed as a try extension of cli
    raise NotImplementedError()


@bp.route("/Workspace/<name>/CommandTree/Nodes/<path:command_group>/Leaves/<command>/Try", methods=("POST",))
def editor_workspace_try_command(name, command_group, command):
    root_node_names = command_group.split('/')
    if root_node_names[0] != WorkspaceManager.COMMAND_TREE_ROOT_NAME:
        raise exceptions.ResourceNotFind("Command not exist")
    root_node_names = root_node_names[1:]

    manager = WorkspaceManager(name)
    manager.load()
    if not manager.find_command_tree_leaf(*root_node_names, command):
        raise exceptions.ResourceNotFind("Command not exist")

    # try command by installed as a try extension of cli
    raise NotImplementedError()
