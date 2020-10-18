# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/Projects/MayaSceneExporter/Maya/SceneExporter/SceneExporterQWidget.ui'
#
# Created: Sun Oct 18 16:05:54 2020
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SceneExporter(object):
    def setupUi(self, SceneExporter):
        SceneExporter.setObjectName("SceneExporter")
        SceneExporter.resize(595, 254)
        self.gridLayout = QtWidgets.QGridLayout(SceneExporter)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(SceneExporter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_export_fbx = QtWidgets.QPushButton(self.groupBox)
        self.btn_export_fbx.setObjectName("btn_export_fbx")
        self.gridLayout_2.addWidget(self.btn_export_fbx, 0, 0, 1, 1)
        self.btn_export_json = QtWidgets.QPushButton(self.groupBox)
        self.btn_export_json.setObjectName("btn_export_json")
        self.gridLayout_2.addWidget(self.btn_export_json, 0, 1, 1, 1)
        self.btn_export_fbx_and_json = QtWidgets.QPushButton(self.groupBox)
        self.btn_export_fbx_and_json.setObjectName("btn_export_fbx_and_json")
        self.gridLayout_2.addWidget(self.btn_export_fbx_and_json, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(SceneExporter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.json_dir_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.json_dir_edit.setObjectName("json_dir_edit")
        self.gridLayout_3.addWidget(self.json_dir_edit, 1, 1, 1, 1)
        self.fbx_dir_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.fbx_dir_edit.setObjectName("fbx_dir_edit")
        self.gridLayout_3.addWidget(self.fbx_dir_edit, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 3, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(SceneExporter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(SceneExporter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 2)

        self.retranslateUi(SceneExporter)
        QtCore.QMetaObject.connectSlotsByName(SceneExporter)

    def retranslateUi(self, SceneExporter):
        SceneExporter.setWindowTitle(QtWidgets.QApplication.translate("SceneExporter", "Scene Exporter", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("SceneExporter", "Export selected objects in Scene", None, -1))
        self.btn_export_fbx.setText(QtWidgets.QApplication.translate("SceneExporter", "FBX Only", None, -1))
        self.btn_export_json.setText(QtWidgets.QApplication.translate("SceneExporter", "JSON Only", None, -1))
        self.btn_export_fbx_and_json.setText(QtWidgets.QApplication.translate("SceneExporter", "FBX and JSON", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("SceneExporter", "Settings", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("SceneExporter", "JSON Export Folder:", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("SceneExporter", "FBX Export Folder:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("SceneExporter", "Settings are stored in scene node named SceneExporter.", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("SceneExporter", "Exports objects in selected groups as FBX files with JSON file for group containing object transform information.", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("SceneExporter", "When multiple objects share the same shape, only one FBX will be created.", None, -1))
