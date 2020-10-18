"""
Identifies and exports objects in selected groups as FBX and JSON files.

This code should be kept seperate from tool UI.
"""
import os
import json
import logging

import maya.cmds as cmds


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def export_selected_groups(fbx_export_dir, json_export_dir):
	"""
	Exports objects in selected groups as fbx files with json file for transform info.

	Parameters
	----------
	fbx_export_dir: FBX Export dir.
	json_export_dir: JSON Export dir.
	"""
	# todo: Ensure only groups are selected
	selected_groups = cmds.ls(selection=True, long=True)
	if not selected_groups:
		cmds.warning('No groups selected')
		return

	for group in selected_groups:
		export(group, fbx_export_dir, json_export_dir)

	# Restore selection
	cmds.select(selected_groups, replace=True)


def export(group_full_path, fbx_export_dir, json_export_dir):
	"""
	Exports objects in group as fbx files with json file for transform info.

	Parameters
	----------
	group_full_path: Full path to the group containing child objects for export
	fbx_export_dir: FBX Export dir.
	json_export_dir: JSON Export dir.
	"""
	# todo: Ensure only mesh objects get returned
	transform_nodes = cmds.listRelatives(group_full_path, children=True, fullPath=True) or []
	if not transform_nodes:
		cmds.warning('Group {} contains no child objects')
		return

	group_name = _get_short_name(group_full_path)
	LOG.info('Exporting objects for group ' + group_name)

	export_nodes, json_scene_nodes = _parse_objects(transform_nodes)

	if fbx_export_dir:
		for node in export_nodes:
			_export_node_to_fbx(node, fbx_export_dir)

	if json_export_dir:
		_export_json_objects(json_export_dir, group_name, json_scene_nodes)


def _export_node_to_fbx(node, export_dir):
	short_name = _get_short_name(node)
	LOG.info('Export {}.fbx'.format(node))
	LOG.debug('Selecting only {}'.format(node))
	cmds.select(node, replace=True)
	fbx_path = os.path.join(export_dir, short_name + '.fbx').replace('\\', '/')

	# todo: Clear fbx export settings first?

	# We need to set node matrix back to identity before export,
	# so save backup of matrix to restore afterwards
	matrix_to_restore = cmds.xform(node, matrix=True, query=True, worldSpace=True)
	cmds.makeIdentity(node)

	try:
		cmds.file(fbx_path, force=True, options="v = 0", type="FBX export", exportSelected=True)
	finally:
		cmds.xform(node, matrix=matrix_to_restore)


def _export_json_objects(export_dir, group_name, json_scene_nodes):
	json_path = os.path.join(export_dir, group_name + '.SceneExport.json')

	with open(json_path, 'w') as f:
		json_dict = {'name': group_name, 'items': json_scene_nodes}
		json.dump(json_dict, f)


def _parse_objects(transform_nodes):
	"""
	Returns a list of objects for export to FBX and
	list of objects to include in exported JSON
	"""
	export_nodes = []
	shared_shapes = {}
	
	# Will hold all the info about instance transform in scene
	json_scene_nodes = []

	for t in transform_nodes:
		shape = _get_transform_shape(t)
		LOG.debug('Fetching parents for ' + shape)
		parents = cmds.listRelatives(shape, allParents=True, fullPath=True)

		if len(parents) > 1:
			LOG.debug('Found multiple parents for ' + shape)
			# Shared shape
			original_node = shared_shapes.get(t, None)

			if original_node:
				LOG.debug('Create instance of {} in scene called {}'.format(original_node, t))
			else:
				original_node = parents[0]
				export_nodes.append(original_node)
				LOG.debug('Adding new original node called {} for scene instance {}'.format(original_node, t))

				for p in parents:
					shared_shapes[p] = original_node

			json_scene_nodes.append(_add_json_scene_node(original_node, t))
		else:
			LOG.debug('Adding basic node called {}'.format(t))
			original_node = t
			json_scene_nodes.append(_add_json_scene_node(original_node, t))
			export_nodes.append(t)

	return export_nodes, json_scene_nodes


def _add_json_scene_node(original_name, instance_name):
	return {'fbx': _get_short_name(original_name), 'name': _get_short_name(instance_name), 'transform': _get_transform_matrix(instance_name)}


def _get_transform_matrix(t):
	return cmds.xform(t, matrix=True, query=True, worldSpace=True)


def _get_transform_shape(transform_name):
	shapes = cmds.listRelatives(transform_name, shapes=True, fullPath=True)
	return shapes[0]


def _get_short_name(long_name):
	return long_name.rsplit('|', 1)[1]
