# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
import qt_maya_utils as QtMayaUtils
from rigging_system_commands import SkeletonRiggingCommands
from output_system_commands import OutputLog

class SkeletonTabWidget(WidgetTemplate.QtMayaNestedWidget):

    def __init__(self, widget_container, parent_window_instance):
        self.parent_window = parent_window_instance

        super().__init__(widget_container)

    def _collect_ui_elements(self):
        self.btn_skeletonNewJoint = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_skeletonNewJoint')
        self.btn_loadRigTemplate = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_loadRigTemplate')
        self.btn_saveRigTemplate = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_saveRigTemplate')
        self.btn_mirrorRig = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_mirrorRig')

        self.list_skeletonRootJoint = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_skeletonRootJoint')
        self.list_RigTemplate = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_RigTemplate')

        self.lineEdit_TemplateName = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_TemplateName')
        self.lineEdit_MirrorRigSearch = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_MirrorRigSearch')
        self.lineEdit_MirrorRigReplace = self.QWidget_instance.findChild(QtWidgets.QLineEdit, 'lineEdit_MirrorRigReplace')

        self.btnGrp_jointMirrorAxis = self.parent_window.findChild(QtWidgets.QButtonGroup, 'btnGrp_jointMirrorAxis')

        return

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        self.btn_skeletonNewJoint.clicked.connect(self._on_btn_skeletonNewJoint_clicked)
        self.btn_loadRigTemplate.clicked.connect(self._on_btn_loadRigTemplate_clicked)
        self.btn_saveRigTemplate.clicked.connect(self._on_btn_saveRigTemplate_clicked)
        self.btn_mirrorRig.clicked.connect(self._on_btn_mirrorRig_clicked)

        self.list_skeletonRootJoint.itemClicked.connect(self._on_list_skeletonRootJoint_item_clicked)

        return

    def _call_output_update(self):
        """
        Calls SimpleRigtoolWindowWidget function for populate output widget
        """
        self.parent_window.populate_output_widget()
        return

    def _on_btn_skeletonNewJoint_clicked(self):
        # get selected maya obj, validate, set

        self._assign_selected_joint_as_new_rig_root_joint()
        self._call_output_update()
        return

    def _assign_selected_joint_as_new_rig_root_joint(self):
        is_success, new_joint = _DataHandler.update_rig_root_joint()

        if is_success:
            self._update_rig_root_joint(new_joint)

        return


    def _update_rig_root_joint(self, new_root_joint):
        """
        Removes prior item, adds new item
        :param new_root_joint: string entry
        """

        self.list_skeletonRootJoint.takeItem(0)
        self.list_skeletonRootJoint.addItem(new_root_joint)

        return

    def _on_btn_loadRigTemplate_clicked(self):
        print("btn_loadRigTemplate")

        # TODO: complete UI task
        self._load_rig_template()
        self._call_output_update()

        return

    def _load_rig_template(self):
        template_to_load = self.list_RigTemplate.selectedItems()

        if template_to_load:

            print(template_to_load[0].text())
            _DataHandler.load_rig_template(template_to_load[0].text())

        else:
            OutputLog.add_to_output_log("-Please select a template", "")

        return

    def _on_btn_saveRigTemplate_clicked(self):
        print("btn_saveRigTemplate")

        # TODO: complete UI task
        self._save_rig_template()
        self._call_output_update()

        return

    def _save_rig_template(self):
        # get root joint hierarchy
        # read list
        # TODO: complete UI task
        new_template_name = self.lineEdit_TemplateName.text()

        if new_template_name:
            _DataHandler.save_rig_template(new_template_name)

        else:
            OutputLog.add_to_output_log("-Please enter a template name", "")

        print(new_template_name)
        return


    def _on_btn_mirrorRig_clicked(self):
        print("btn_mirrorRig")
        # TODO: complete UI task
        self._mirror_root_rig_hierarchy()
        self._call_output_update()

        return


    def _mirror_root_rig_hierarchy(self):
        search_text = self.lineEdit_MirrorRigSearch.text()
        replace_text = self.lineEdit_MirrorRigReplace.text()
        mirror_axis = self.btnGrp_jointMirrorAxis.checkedId()

        print(f"Search {search_text}, Replace {replace_text}, Mirror Option {mirror_axis}")

        _DataHandler.mirror_root_rig(search_text=search_text, replace_text=replace_text,
                                     mirrorAxisRadioButtonID=mirror_axis)


    def _on_list_skeletonRootJoint_item_clicked(self, item_clicked):
        print("list_skeletonRootJoint")
        # TODO: complete UI task
        _DataHandler.select_current_rig_root_joint_in_maya()
        self._call_output_update()
        return



class _DataHandler:
    """
    
    """

    @classmethod
    def update_rig_root_joint(cls):
        new_root_joint = QtMayaUtils.get_user_selected_maya_objects()
        is_success = SkeletonRiggingCommands.set_rig_root_joint(new_root_joint)

        if is_success:
            new_joint_name = str(new_root_joint[0])

        else:
            new_joint_name = ""

        return is_success, new_joint_name


    @classmethod
    def load_rig_template(cls, template_name):
        SkeletonRiggingCommands.load_rig_template(template_name)
        return

    @classmethod
    def save_rig_template(cls, template_name):
        SkeletonRiggingCommands.save_rig_template_from_metadata_joint_rig(template_name)
        return

    @classmethod
    def mirror_root_rig(cls, search_text, replace_text, mirrorAxisRadioButtonID):
        # -2 - YZ
        # -3 - XY
        # -4 - ZX

        if mirrorAxisRadioButtonID == -2:
            mirrorXY = False
            mirrorYZ = True
            mirrorZX = False
        elif mirrorAxisRadioButtonID == -3:
            mirrorXY = True
            mirrorYZ = False
            mirrorZX = False
        else:
            mirrorXY = False
            mirrorYZ = False
            mirrorZX = True


        SkeletonRiggingCommands.mirror_rig_on_metadata_joint_rig(search_text=search_text, replace_text=replace_text,
                                                                 mirrorXY=mirrorXY, mirrorYZ=mirrorYZ,
                                                                 mirrorZX=mirrorZX)

        return

    @classmethod
    def select_current_rig_root_joint_in_maya(cls):
        object_to_select = SkeletonRiggingCommands.get_current_rig_root_joint()
        QtMayaUtils.select_maya_object(object_to_select)
        return
