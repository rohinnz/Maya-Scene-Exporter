"""
Tool for exporting objects as FBX files with JSON info for scene transforms.

Allows for scene to be built using repeatable objects in Maya with one click export.
"""
import json
import logging

import maya.OpenMayaUI
import shiboken2
import maya.cmds as cmds
from PySide2 import QtCore, QtWidgets

import exporter
import SceneExporterQWidget


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


class SceneExporterApp(QtWidgets.QWidget):
	def __init__(self):
		# Attach to Maya main window
		self._maya_main_window = get_maya_main_window()
		super(SceneExporterApp, self).__init__(parent=self._maya_main_window)
		self.setWindowFlags(QtCore.Qt.Window)

		# Setup UI
		self._ui = SceneExporterQWidget.Ui_SceneExporter()
		self._ui.setupUi(self)

		# Load previous values from settings
		self._settings = Settings()
		self._settings.load()
		self._ui.fbx_dir_edit.setText(self._settings.fbx_dir)
		self._ui.json_dir_edit.setText(self._settings.json_dir)

		# Setup callbacks
		self._ui.fbx_dir_edit.textEdited.connect(self._on_fbx_dir_edited)
		self._ui.json_dir_edit.textEdited.connect(self._on_json_dir_edited)

		self._ui.btn_export_fbx_and_json.clicked.connect(self._fbx_and_json_export_clicked)
		self._ui.btn_export_fbx.clicked.connect(self._fbx_only_export_clicked)
		self._ui.btn_export_json.clicked.connect(self._json_only_export_clicked)

		self._ui.btn_browse_fbx_dir.clicked.connect(self._browse_fbx_dir_clicked)
		self._ui.btn_browse_json_dir.clicked.connect(self._browse_json_dir_clicked)

		# Finally show the app
		self.show()

	def _on_fbx_dir_edited(self, text):
		self._settings.fbx_dir = text
		self._settings.save()

	def _on_json_dir_edited(self, text):
		self._settings.json_dir = text
		self._settings.save()

	def _fbx_and_json_export_clicked(self):
		exporter.export_selected_groups(self._settings.fbx_dir, self._settings.json_dir)

	def _json_only_export_clicked(self):
		exporter.export_selected_groups(None, self._settings.json_dir)

	def _fbx_only_export_clicked(self):
		exporter.export_selected_groups(self._settings.fbx_dir, None)

	def _browse_fbx_dir_clicked(self):
		new_dir = self._show_dir_browser("Select FBX Export Directory", self._ui.fbx_dir_edit.text())
		if new_dir:
			self._ui.fbx_dir_edit.setText(new_dir)
			self._on_fbx_dir_edited(new_dir)

	def _browse_json_dir_clicked(self):
		new_dir = self._show_dir_browser("Select JSON Export Directory", self._ui.json_dir_edit.text())
		if new_dir:
			self._ui.json_dir_edit.setText(new_dir)
			self._on_json_dir_edited(new_dir)

	def _show_dir_browser(self, title, existing_dir):
		return QtWidgets.QFileDialog.getExistingDirectory(self, title, existing_dir, QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

# ----------------------------------------------------------------------------------------------------------------------
# Utils


def get_maya_main_window():
	main_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
	return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

# ----------------------------------------------------------------------------------------------------------------------
# Settings


SETTINGS_NODE_NAME = 'SceneExporterSettings'
SETTINGS_NODE_ATTR = 'json_data'


class Settings(object):
	def __init__(self):
		self.fbx_dir = ''
		self.json_dir = ''

	def load(self):
		json_str = self._get_settings_json_string()
		if not json_str:
			return

		loaded_dict = json.loads(json_str)
		for key, value in loaded_dict.items():
			self.__dict__[key] = value

	def save(self):
		json_str = json.dumps(self.__dict__)
		self._set_settings_json_string(json_str)

	@staticmethod
	def _get_settings_json_string():
		if cmds.objExists('|' + SETTINGS_NODE_NAME):
			return cmds.getAttr('|{}.{}'.format(SETTINGS_NODE_NAME, SETTINGS_NODE_ATTR))
		else:
			return None

	@staticmethod
	def _set_settings_json_string(json_string):
		if not cmds.objExists('|' + SETTINGS_NODE_NAME):
			cmds.createNode('transform', n=SETTINGS_NODE_NAME)
			cmds.addAttr('|' + SETTINGS_NODE_NAME, longName=SETTINGS_NODE_ATTR, dataType='string')

		cmds.setAttr("|{}.{}".format(SETTINGS_NODE_NAME, SETTINGS_NODE_ATTR), json_string, type='string')

