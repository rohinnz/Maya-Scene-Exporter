import os
import json
import logging

import maya.cmds as cmds
import maya.mel as mel


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def export(group_name, transform_nodes, fbx_export_dir, json_export_dir):
	"""

	Parameters
	----------
	group_name: Used in filename of scene export json file
	transform_nodes: All nodes to process for exporting
	export_dir: Directory to export fbx and json files.
	"""
	export_nodes, json_scene_nodes = parse_objects(transform_nodes)

	for node in export_nodes:
		export_node_to_fbx(node, fbx_export_dir)

	export_json_objects(json_export_dir, group_name, json_scene_nodes)


def export_node_to_fbx(node, export_dir):
	short_name = get_short_name(node)
	LOG.info('Export {}.fbx'.format(node))
	LOG.debug('Selecting only {}'.format(node))
	cmds.select(node, replace=True)
	fbx_path = os.path.join(export_dir, short_name + '.fbx').replace('\\', '/')

	# todo: Clear fbx export settings first?

	cmds.file(fbx_path, force=True, options="v = 0", type="FBX export", exportSelected=True)


def export_json_objects(export_dir, group_name, json_scene_nodes):
	json_path = os.path.join(export_dir, group_name + '.SceneExport.json')

	with open(json_path, 'w') as f:
		json_dict = {'name': group_name, 'items': json_scene_nodes}
		json.dump(json_dict, f)


def parse_objects(transform_nodes):
	"""
	Returns a list of objects for export to FBX and
	list of objects to include in exported JSON
	"""
	export_nodes = []
	shared_shapes = {}
	
	# Will hold all the info about instance transform in scene
	json_scene_nodes = []

	for t in transform_nodes:
		shape = get_transform_shape(t)
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

			json_scene_nodes.append(add_json_scene_node(original_node, t))
		else:
			LOG.debug('Adding basic node called {}'.format(t))
			original_node = t
			json_scene_nodes.append(add_json_scene_node(original_node, t))
			export_nodes.append(t)

	return export_nodes, json_scene_nodes


def add_json_scene_node(original_name, instance_name):
	return {'fbx': get_short_name(original_name), 'name': get_short_name(instance_name), 'transform': get_transform_matrix(instance_name)}


def get_transform_matrix(t):
	return cmds.xform(t, matrix=True, query=True, worldSpace=True)


def get_transform_shape(transform_name):
	shapes = cmds.listRelatives(transform_name, shapes=True, fullPath=True)
	return shapes[0]


def get_short_name(long_name):
	return long_name.rsplit('|', 1)[1]
