from __future__ import print_function
import maya.cmds as cmds

import exporter


def show():
	raise NotImplementedError('Scene Exporter UI still work in progress')


def export_selected(fbx_export_dir, json_export_dir):
	selected_objs = cmds.ls(selection=True, long=True)
	if not selected_objs:
		cmds.warning('No objects selected')
		return

	group_name = exporter.get_short_name(selected_objs[0])
	exporter.export(group_name, selected_objs, fbx_export_dir, json_export_dir)
