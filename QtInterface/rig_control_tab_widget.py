# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
import qt_maya_utils as QtMayaUtils


class RigControlTabWidget(WidgetTemplate.QtMayaNestedWidget):

    def __init__(self, widget_container, parent_window_instance):
        self.parent_window = parent_window_instance

        super().__init__(widget_container)


    def _collect_ui_elements(self):
        self.btn_assignTargetControl = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_assignTargetControl')
        self.btn_assignTargetJoint = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_assignTargetJoint')
        self.btn_createControl = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_createControl')
        self.btn_mirrorControls = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_mirrorControls')

        self.btn_constrainParent = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_constrainParent')
        self.btn_constrainPoint = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_constrainPoint')
        self.btn_constrainPoleVector = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_constrainPoleVector')

        self.list_targetControl = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_targetControl')
        self.list_rigControl_targetJoint = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_rigControl_targetJoint')

        self.lineEdit_mirrorControlSearch = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_mirrorControlSearch')
        self.lineEdit_mirrorControlReplace = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_mirrorControlReplace')

        self.btnGrp_controlMirrorAxis = self.parent_window.findChild(QtWidgets.QButtonGroup, 'btnGrp_controlMirrorAxis')

        self.checkBox_constrainRotation = self.QWidget_instance.findChild(QtWidgets.QCheckBox, 'checkBox_constrainRotation')
        self.checkBox_constrainScale = self.QWidget_instance.findChild(QtWidgets.QCheckBox,
                                                                          'checkBox_constrainScale')
        self.checkBox_constrainTranslate = self.QWidget_instance.findChild(QtWidgets.QCheckBox,
                                                                          'checkBox_constrainTranslate')

        self.doubleSpinBox_controlScale = self.QWidget_instance.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_controlScale')
        self.doubleSpinBox_controlRotX = self.QWidget_instance.findChild(QtWidgets.QDoubleSpinBox,
                                                                          'doubleSpinBox_controlRotX')
        self.doubleSpinBox_controlRotY = self.QWidget_instance.findChild(QtWidgets.QDoubleSpinBox,
                                                                          'doubleSpinBox_controlRotY')
        self.doubleSpinBox_controlRotZ = self.QWidget_instance.findChild(QtWidgets.QDoubleSpinBox,
                                                                          'doubleSpinBox_controlRotZ')
        return

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        self.btn_assignTargetControl.clicked.connect(self._on_btn_assignTargetControl_clicked)
        self.btn_assignTargetJoint.clicked.connect(self._on_btn_assignTargetJoint_clicked)
        self.btn_createControl.clicked.connect(self._on_btn_createControl_clicked)
        self.btn_mirrorControls.clicked.connect(self._on_btn_mirrorControls_clicked)
        self.btn_constrainParent.clicked.connect(self._on_btn_constrainParent_clicked)
        self.btn_constrainPoint.clicked.connect(self._on_btn_constrainPoint_clicked)
        self.btn_constrainPoleVector.clicked.connect(self._on_btn_constrainPoleVector_clicked)

        self.list_targetControl.itemClicked.connect(self._on_list_targetControl_item_clicked)
        self.list_rigControl_targetJoint.itemClicked.connect(self._on_list_rigControl_targetJoint_item_clicked)

        return

    def _on_btn_assignTargetControl_clicked(self):
        print("btn_assignTargetControl")
        # get maya obj
        return

    def _on_btn_assignTargetJoint_clicked(self):
        print("btn_assignTargetJoint")
        # get maya obj

        return


    def _on_btn_createControl_clicked(self):
        print("btn_createControl")
        self._create_control()
        return

    def _create_control(self):
        scale = self.doubleSpinBox_controlScale.value()
        rotation = (self.doubleSpinBox_controlRotX.value(),
                    self.doubleSpinBox_controlRotY.value(),
                    self.doubleSpinBox_controlRotZ.value())
        print(f"Scale: {scale}. Rotation: {rotation}")
        return

    def _on_btn_mirrorControls_clicked(self):
        print("btn_mirrorControls")

        self._mirror_control_hierarchy()

        return

    def _mirror_control_hierarchy(self):
        search_text = self.lineEdit_mirrorControlSearch.text()
        replace_text = self.lineEdit_mirrorControlReplace.text()
        mirror_axis = self.btnGrp_controlMirrorAxis.checkedId()

        print(f"Search {search_text}, Replace {replace_text}, Mirror Option {mirror_axis}")

    def _on_btn_constrainParent_clicked(self):
        print("btn_constrainParent")

        self._parent_constrain_control_on_joint()

        return

    def _parent_constrain_control_on_joint(self):
        translate, rotation, scale = (self.checkBox_constrainTranslate.isChecked(),
                                      self.checkBox_constrainRotation.isChecked(),
                                      self.checkBox_constrainScale.isChecked())

        print(f"Translate: {translate}, Rotation: {rotation}, Scale: {scale}")


    def _on_btn_constrainPoint_clicked(self):
        print("btn_constrainPoint")

        return


    def _on_btn_constrainPoleVector_clicked(self):
        print("btn_constrainPoleVector")

        return

    def _on_list_targetControl_item_clicked(self, item_clicked):
        print("list_targetControl")

        return

    def _on_list_rigControl_targetJoint_item_clicked(self, item_clicked):
        print("list_rigControl_targetJoint")

        return
