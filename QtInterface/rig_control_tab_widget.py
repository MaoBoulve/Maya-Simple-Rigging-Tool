# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
import qt_maya_utils as QtMayaUtils
from rigging_system_commands import RigControlCommands


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

        self.lineEdit_jointNotation = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_jointNotation')
        self.lineEdit_controlNotation = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_controlNotation')

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

    def _call_output_update(self):
        """
        Calls SimpleRigtoolWindowWidget function for populate output widget
        """
        self.parent_window.populate_output_widget()
        return

    def _on_btn_assignTargetControl_clicked(self):
        print("btn_assignTargetControl")
        # get maya obj
        self._assign_selected_control_as_new_target_control()
        self._call_output_update()
        return

    def _assign_selected_control_as_new_target_control(self):


        is_success, new_control = _DataHandler.update_target_control()

        if is_success:
            self._update_target_control(new_control)

        return

    def _update_target_control(self, new_control):
        """
        Removes prior item, adds new item
        :param new_control: string entry
        """

        self.list_targetControl.takeItem(0)
        self.list_targetControl.addItem(new_control)

        return


    def _on_btn_assignTargetJoint_clicked(self):
        print("btn_assignTargetJoint")
        # get maya obj

        self._assign_selected_joint_as_new_target_joint()
        self._call_output_update()
        return

    def _assign_selected_joint_as_new_target_joint(self):


        is_success, new_joint = _DataHandler.update_target_joint()

        if is_success:
            self._update_target_joint(new_joint)

        return


    def _update_target_joint(self, new_joint):
        """
        Removes prior item, adds new item
        :param new_joint: string entry
        """

        self.list_rigControl_targetJoint.takeItem(0)
        self.list_rigControl_targetJoint.addItem(new_joint)

        return


    def _on_btn_createControl_clicked(self):
        print("btn_createControl")
        self._create_control()
        self._call_output_update()
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
        self._call_output_update()

        return

    def _mirror_control_hierarchy(self):
        search_text = self.lineEdit_mirrorControlSearch.text()
        replace_text = self.lineEdit_mirrorControlReplace.text()
        mirror_axis = self.btnGrp_controlMirrorAxis.checkedId()

        print(f"Search {search_text}, Replace {replace_text}, Mirror Option {mirror_axis}")

    def _on_btn_constrainParent_clicked(self):
        print("btn_constrainParent")

        self._parent_constrain_control_on_joint()
        self._call_output_update()

        return

    def _parent_constrain_control_on_joint(self):
        translate, rotation, scale = (self.checkBox_constrainTranslate.isChecked(),
                                      self.checkBox_constrainRotation.isChecked(),
                                      self.checkBox_constrainScale.isChecked())

        print(f"Translate: {translate}, Rotation: {rotation}, Scale: {scale}")


    def _on_btn_constrainPoint_clicked(self):
        print("btn_constrainPoint")
        self._call_output_update()

        return


    def _on_btn_constrainPoleVector_clicked(self):
        print("btn_constrainPoleVector")
        self._call_output_update()
        return

    def _on_list_targetControl_item_clicked(self, item_clicked):
        print("list_targetControl")
        self._call_output_update()
        return

    def _on_list_rigControl_targetJoint_item_clicked(self, item_clicked):
        print("list_rigControl_targetJoint")
        self._call_output_update()
        return

class _DataHandler:
    """

    """

    @classmethod
    def update_target_control(cls):
        new_control = QtMayaUtils.get_user_selected_maya_objects()
        is_success = RigControlCommands.set_target_control(new_control)

        if is_success:
            new_control_name = str(new_control[0])

        else:
            new_control_name = ""

        return is_success, new_control_name

    @classmethod
    def update_target_joint(cls):
        new_joint = QtMayaUtils.get_user_selected_maya_objects()
        is_success = RigControlCommands.set_new_target_joint(new_joint)

        if is_success:
            new_joint_name = str(new_joint[0])

        else:
            new_joint_name = ""

        return is_success, new_joint_name