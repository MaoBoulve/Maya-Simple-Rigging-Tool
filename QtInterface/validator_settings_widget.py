# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.



"""
Qt Validator Settings Widget. Nests Widget classes in the main settings widget with use of Qt Tabs.
"""
from abc import abstractmethod

import qt_maya_widget_base as WidgetTemplate
from PySide2 import QtWidgets

from qt_utils import QtMayaUtils

from validator_commands import BackEndCommands


class SettingsWidget(WidgetTemplate.QtMayaWidgetWindow):
    """
    Validator Settings Qt Widget for setting parameters for validation

    Qt Classes used:
    -QPushButton
    -QTabWidget
    """

    tab_order_dict = {
        0: "character",
        1: "animation",
        2: "prop"
    }

    def __init__(self):

        self.tab_validationTasks = None
        self.btn_run = None
        self.btn_close = None
        self.btn_open_tagging = None
        self.btn_run_all = None

        self.anim_tab = None
        self.prop_tab = None
        self.char_tab = None

        self.previous_run_group_index = None

        super().__init__(filepath=__file__, window_title="Validation Settings", window_object_name="validatorCommands")

        return

    def _collect_ui_elements(self):

        self.btn_close = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_close')
        self.btn_open_tagging = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_open_tagging')
        self.btn_run = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_run')
        self.btn_run_all = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_run_all')
        self.tab_validationTasks = self.QWidget_instance.findChild(QtWidgets.QTabWidget, 'tab_validationTasks')

        return

    def _initialize_ui_element_states(self):

        self.anim_tab = _AnimGroupWidgetTab(tab_widget_parent=self.QWidget_instance)
        self.prop_tab = _PropGroupWidgetTab(tab_widget_parent=self.QWidget_instance)
        self.char_tab = _CharacterGroupWidgetTab(tab_widget_parent=self.QWidget_instance)

        return

    def _create_ui_connections_to_class_functions(self):
        self.btn_close.clicked.connect(self.__on_btn_close_clicked)
        self.btn_open_tagging.clicked.connect(self.__on_btn_open_tagging_clicked)
        self.btn_run.clicked.connect(self.__on_btn_run_clicked)
        self.btn_run_all.clicked.connect(self.__on_btn_run_all_clicked)

    def __on_btn_close_clicked(self):

        # update validation settings on widget
        self.__update_all_validation_settings()

        self._close_window()
        return

    @classmethod
    def __on_btn_open_tagging_clicked(cls):
        _DataHandler.open_tagging_widget()

        return

    def __on_btn_run_clicked(self):

        tab_index = self.tab_validationTasks.currentIndex()
        self.__run_validation_group_by_index(tab_index)

        return

    def __run_validation_group_by_index(self, tab_index):
        """
        Converts current tab index to dictionary (for easier code parsing)
        Runs widget from current settings
        """

        self.previous_run_group_index = tab_index
        task_group_to_run = SettingsWidget.tab_order_dict[tab_index]

        if task_group_to_run == "character":
            self.__run_character_group_validation()

        elif task_group_to_run == "animation":
            self.__run_animation_group_validation()

        elif task_group_to_run == "prop":
            self.__run_prop_group_validation()

        return

    def __run_character_group_validation(self):
        """
        Collects settings and runs character validation
        """
        tab_params = self.char_tab.get_current_tab_parameters()
        _DataHandler.run_character_validation(tab_params)

        return

    def __run_animation_group_validation(self):
        """
        Collects settings and runs animation validation
        """
        tab_params = self.anim_tab.get_current_tab_parameters()
        _DataHandler.run_animation_validation(tab_params)

        return

    def __run_prop_group_validation(self):
        """
        Collects settings and runs character validation
        """

        tab_params = self.prop_tab.get_current_tab_parameters()
        _DataHandler.run_prop_validation(tab_params)

        return

    def __update_all_validation_settings(self):
        """
        Updates all validation settings
        """

        tab_params = self.anim_tab.get_current_tab_parameters()
        _DataHandler.update_anim_validation_settings(tab_params)

        tab_params = self.char_tab.get_current_tab_parameters()
        _DataHandler.update_char_validation_settings(tab_params)

        tab_params = self.prop_tab.get_current_tab_parameters()
        _DataHandler.update_prop_validation_settings(tab_params)

        return

    def __on_btn_run_all_clicked(self):
        """
        Runs all validation groups
        """

        self.__run_all_validation_groups()
        return

    def __run_all_validation_groups(self):
        """
        Calls all validation group calls
        """

        self.previous_run_group_index = -1

        self.__update_all_validation_settings()
        _DataHandler.run_all_validation_groups()

        return

    def rerun_validation(self):
        """
        Public function to rerun previous validation
        """
        if self.previous_run_group_index == -1:
            self.__run_all_validation_groups()
        else:
            self.__run_validation_group_by_index(self.previous_run_group_index)
        return


class _CommandWidgetTabBase(WidgetTemplate.QtMayaWidget):
    """
    Base class for widget tabs.
    Do not require loading Qt file so derive from base Maya Widget Class
    """

    def __init__(self, tab_widget_parent):
        """
        Init call
        """
        self.widget_parent = tab_widget_parent
        super().__init__()
        return

    def _init_ui_file(self):
        """
        Does not need .ui file for tabs
        """
        pass

    @abstractmethod
    def get_current_tab_parameters(self):
        """
        Returns widget tab dictionary parameters
        """
        tab_params = {}

        return tab_params


class _AnimGroupWidgetTab(_CommandWidgetTabBase):

    def __init__(self, tab_widget_parent):
        # ui elements
        self.btnGrp_attributeOption = None
        self.btnGrp_keyframeRangeOption = None
        self.input_minKeyframe = None
        self.input_maxKeyframe = None
        self.check_translate = None
        self.check_rotate = None
        self.check_scale = None
        self.check_visible = None

        # parameter to return
        self.min_frame = None
        self.max_frame = None
        self.attributes_to_check = None

        super().__init__(tab_widget_parent)

        return

    def _collect_ui_elements(self):
        self.btnGrp_attributeOption = self.widget_parent.findChild(QtWidgets.QButtonGroup, 'btnGrp_attribOption')
        self.btnGrp_keyframeRangeOption = self.widget_parent.findChild(QtWidgets.QButtonGroup, 'btnGrp_keyRange')

        self.input_minKeyframe = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_minKeyframe')
        self.input_maxKeyframe = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_maxKeyframe')

        self.check_translate = self.widget_parent.findChild(QtWidgets.QCheckBox, 'check_translate')
        self.check_rotate = self.widget_parent.findChild(QtWidgets.QCheckBox, 'check_rotate')
        self.check_scale = self.widget_parent.findChild(QtWidgets.QCheckBox, 'check_scale')
        self.check_visible = self.widget_parent.findChild(QtWidgets.QCheckBox, 'check_visible')

        return

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        pass

    def get_current_tab_parameters(self):
        """
        Returns animation group settings:

        dict [tab_params] = {

        "min_frame": int,

        "max_frame": int,

        "attributes": list of string

        }
        """
        self.__reset_parameters()

        self.__check_keyframe_parameter_settings()

        tab_params = {"min_frame": self.min_frame,
                      "max_frame": self.max_frame, "attributes": self.attributes_to_check
                      }

        return tab_params

    def __reset_parameters(self):
        """Resets parameters"""

        self.min_frame = None
        self.max_frame = None

        self.attributes_to_check = None

        return

    def __check_keyframe_parameter_settings(self):
        """Check if custom user settings or default setting should be used"""
        self.__check_if_custom_attributes()
        self.__check_if_custom_keyframe_range()

        return

    def __check_if_custom_keyframe_range(self):
        """Checks radio button index for custom setting"""
        # -2 is default, -3 is custom

        if self.btnGrp_keyframeRangeOption.checkedId() == -3:
            self.__set_custom_key_range_to_input_entry()

        return

    def __check_if_custom_attributes(self):
        """Checks radio button index for custom setting"""
        # -2 is default, -3 is custom

        if self.btnGrp_attributeOption.checkedId() == -3:
            self.__set_attributes_to_check_to_marked_entries()

        return

    def __set_custom_key_range_to_input_entry(self):
        """Sets keyframes to text from user, validated by UI to int only input"""
        self.min_frame = int(self.input_minKeyframe.text())
        self.max_frame = int(self.input_maxKeyframe.text())

        return

    def __set_attributes_to_check_to_marked_entries(self):
        """Sets attributes to marked entries for keyframe check"""

        self.attributes_to_check = []

        if self.check_translate.isChecked():
            append_string = ['translateX', 'translateY', 'translateZ']
            self.attributes_to_check.extend(append_string)

        if self.check_rotate.isChecked():
            append_string = ['rotateX', 'rotateY', 'rotateZ']
            self.attributes_to_check.extend(append_string)

        if self.check_scale.isChecked():
            append_string = ['scaleX', 'scaleY', 'scaleZ']
            self.attributes_to_check.extend(append_string)

        if self.check_visible.isChecked():
            append_string = ['visibility']
            self.attributes_to_check.extend(append_string)

        return


class _PropGroupWidgetTab(_CommandWidgetTabBase):

    def __init__(self, tab_widget_parent):

        # ui elements
        self.btnGrp_emptyKeyRangeProp = None
        self.input_emptyMinFrameProp = None
        self.input_emptyMaxFrameProp = None
        self.list_sceneMaterials_prop = None
        self.list_validMaterials_prop = None
        self.btn_addValidMaterial_prop = None
        self.btn_removeValidMaterial_prop = None
        self.input_collisionMeshPrefix = None

        # parameter to return
        self.min_empty_frame = None
        self.max_empty_frame = None
        self.valid_materials = None
        self.collision_prefix = None


        super().__init__(tab_widget_parent)

        return

    def _collect_ui_elements(self):
        self.btnGrp_emptyKeyRangeProp = self.widget_parent.findChild(QtWidgets.QButtonGroup, 'btnGrp_emptyKeyRangeProp')

        self.input_emptyMinFrameProp = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_emptyMinFrameProp')
        self.input_emptyMaxFrameProp = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_emptyMaxFrameProp')
        self.input_collisionMeshPrefix = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_collisionMeshPrefix')

        self.list_sceneMaterials_prop = self.widget_parent.findChild(QtWidgets.QListWidget, 'list_sceneMaterials_prop')
        self.list_validMaterials_prop = self.widget_parent.findChild(QtWidgets.QListWidget, 'list_validMaterials_prop')

        self.btn_addValidMaterial_prop = self.widget_parent.findChild(QtWidgets.QPushButton,
                                                                      'btn_addValidMaterial_prop')
        self.btn_removeValidMaterial_prop = self.widget_parent.findChild(QtWidgets.QPushButton,
                                                                         'btn_removeValidMaterial_prop')

        return

    def _initialize_ui_element_states(self):
        """Initialize materials dropdown based on current materials in Maya scene"""
        self.__populate_materials_in_scene_list()

        return

    def __populate_materials_in_scene_list(self):
        """Gets string list of materials and appends to list widget"""
        material_list = QtMayaUtils.get_scene_materials()
        for material in material_list:
            self.list_sceneMaterials_prop.addItem(material)

        return

    def _create_ui_connections_to_class_functions(self):
        self.btn_removeValidMaterial_prop.clicked.connect(self.__on_remove_valid_materials_clicked)
        self.btn_addValidMaterial_prop.clicked.connect(self.__on_add_valid_materials_clicked)

    def __on_add_valid_materials_clicked(self):
        """Moves list widget item from scene materials list to valid materials list"""
        item_to_move = self.list_sceneMaterials_prop.currentItem()

        if item_to_move:
            self.list_validMaterials_prop.addItem(item_to_move.text())

            item_index = self.list_sceneMaterials_prop.row(item_to_move)
            self.list_sceneMaterials_prop.takeItem(item_index)

        return

    def __on_remove_valid_materials_clicked(self):
        """Moves list widget item from valid materials to scene materials"""
        item_to_move = self.list_validMaterials_prop.currentItem()

        if item_to_move:
            self.list_sceneMaterials_prop.addItem(item_to_move.text())

            item_index = self.list_validMaterials_prop.row(item_to_move)
            self.list_validMaterials_prop.takeItem(item_index)

        return

    def get_current_tab_parameters(self):
        """
        Returns prop group settings:

        dict [tab_params] = {

        "min_frame": int,

        "max_frame": int,

        "valid_materials": list of string

        "collision_prefix" : string

        }
        """
        self.__reset_parameters()

        self.__check_keyframe_parameters_settings()

        self.__set_valid_materials_list_to_entries()

        self.__set_collision_prefix_list_to_input_entry()

        tab_params = {"min_frame": self.min_empty_frame,
                      "max_frame": self.max_empty_frame,
                      "valid_materials": self.valid_materials,
                      "collision_prefix": self.collision_prefix
                      }


        return tab_params

    def __reset_parameters(self):
        """Resets parameters on get parameter call"""
        self.min_empty_frame = None
        self.max_empty_frame = None

        self.valid_materials = None

    def __check_keyframe_parameters_settings(self):
        """Checks for default or user validation settings"""
        self.__check_if_custom_key_range()

        return

    def __check_if_custom_key_range(self):
        """Radio button check"""
        # -2 is default, -3 is custom
        if self.btnGrp_emptyKeyRangeProp.checkedId() == -3:
            self.__set_custom_key_range_to_input_entry()

        return

    def __set_custom_key_range_to_input_entry(self):
        """Radio button check"""
        self.min_empty_frame = int(self.input_emptyMinFrameProp.text())
        self.max_empty_frame = int(self.input_emptyMaxFrameProp.text())

        return

    def __set_valid_materials_list_to_entries(self):
        """Sets instance variable from current validMaterials list"""
        self.valid_materials = []
        number_of_items = self.list_validMaterials_prop.count()

        for i in range(number_of_items):
            self.valid_materials.append(self.list_validMaterials_prop.item(i).text())

        return

    def __set_collision_prefix_list_to_input_entry(self):

        self.collision_prefix = self.input_collisionMeshPrefix.text()

        if self.collision_prefix == '':
            self.collision_prefix = None
        else:
            self.collision_prefix = self.collision_prefix.replace(" ", "")
            self.collision_prefix = self.collision_prefix.split(",")

        return


class _CharacterGroupWidgetTab(_CommandWidgetTabBase):

    def __init__(self, tab_widget_parent):

        # ui elements
        self.btnGrp_emptyKeyRange = None
        self.input_emptyMinFrame = None
        self.input_emptyMaxFrame = None
        self.list_sceneMaterials_char = None
        self.list_validMaterials_char = None
        self.btn_addValidMaterial_char = None
        self.btn_removeValidMaterial_char = None

        # parameter to return
        self.min_empty_frame = None
        self.max_empty_frame = None
        self.valid_materials = None

        super().__init__(tab_widget_parent)

        return

    def _collect_ui_elements(self):
        self.btnGrp_emptyKeyRange = self.widget_parent.findChild(QtWidgets.QButtonGroup, 'btnGrp_emptyKeyRange')

        self.input_emptyMinFrame = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_emptyMinFrame')
        self.input_emptyMaxFrame = self.widget_parent.findChild(QtWidgets.QLineEdit, 'input_emptyMaxFrame')

        self.list_sceneMaterials_char = self.widget_parent.findChild(QtWidgets.QListWidget, 'list_sceneMaterials_char')
        self.list_validMaterials_char = self.widget_parent.findChild(QtWidgets.QListWidget, 'list_validMaterials_char')

        self.btn_addValidMaterial_char = self.widget_parent.findChild(QtWidgets.QPushButton,
                                                                      'btn_addValidMaterial_char')
        self.btn_removeValidMaterial_char = self.widget_parent.findChild(QtWidgets.QPushButton,
                                                                         'btn_removeValidMaterial_char')

        return

    def _initialize_ui_element_states(self):
        self.__populate_materials_in_scene_list()

        return

    def __populate_materials_in_scene_list(self):
        """Populates scene materials list"""
        material_list = QtMayaUtils.get_scene_materials()
        for material in material_list:
            self.list_sceneMaterials_char.addItem(material)

        return

    def _create_ui_connections_to_class_functions(self):
        self.btn_removeValidMaterial_char.clicked.connect(self.__on_remove_valid_materials_clicked)
        self.btn_addValidMaterial_char.clicked.connect(self.__on_add_valid_materials_clicked)

        return

    def __on_add_valid_materials_clicked(self):
        """Moves list widget item from scene materials list to valid materials list"""
        item_to_move = self.list_sceneMaterials_char.currentItem()

        if item_to_move:
            self.list_validMaterials_char.addItem(item_to_move.text())

            item_index = self.list_sceneMaterials_char.row(item_to_move)
            self.list_sceneMaterials_char.takeItem(item_index)

        return

    def __on_remove_valid_materials_clicked(self):
        """Moves list widget item from valid materials to scene materials"""
        item_to_move = self.list_validMaterials_char.currentItem()

        if item_to_move:
            self.list_sceneMaterials_char.addItem(item_to_move.text())

            item_index = self.list_validMaterials_char.row(item_to_move)
            self.list_validMaterials_char.takeItem(item_index)

        return

    def get_current_tab_parameters(self):
        """
        Returns character group settings:

        dict [tab_params] = {

        "valid_materials": list of string,

        "min_frame": int,

        "max_frame": int

        }
        """

        self.__reset_parameters()

        self.__check_keyframe_parameters_settings()

        self.__set_valid_materials_list_to_list_entries()

        tab_parameters = {"valid_materials": self.valid_materials,
                          "min_frame": self.min_empty_frame,
                          "max_frame": self.max_empty_frame,
                          }

        return tab_parameters

    def __reset_parameters(self):
        """Resets parameters on get parameter call"""
        self.min_empty_frame = None
        self.max_empty_frame = None

        self.valid_materials = None

        return

    def __check_keyframe_parameters_settings(self):
        """Checks for default or user validation settings"""

        self.__check_if_custom_key_range()

    def __check_if_custom_key_range(self):
        """Radio button check"""

        # -2 is default, -3 is custom
        if self.btnGrp_emptyKeyRange.checkedId() == -3:
            self.__set_custom_key_range_to_input_entry()

        return

    def __set_custom_key_range_to_input_entry(self):
        """Sets keyframes to text from user, validated by UI to int only input"""

        self.min_empty_frame = int(self.input_emptyMinFrame.text())
        self.max_empty_frame = int(self.input_emptyMaxFrame.text())

        return

    def __set_valid_materials_list_to_list_entries(self):
        """Sets instance variable from current validMaterials list"""

        self.valid_materials = []
        number_of_items = self.list_validMaterials_char.count()

        for i in range(number_of_items):
            self.valid_materials.append(self.list_validMaterials_char.item(i).text())

        return


class _DataHandler:
    """
    Handles packing parameters into format for validation tasks to run.

    Isolates dependency on validator hub class to this class
    """

    @staticmethod
    def open_tagging_widget():
        """Call to front end to open asset tagging widget"""
        from validator_commands import FrontEndCommands
        FrontEndCommands.open_asset_tagging_widget()

        return

    @staticmethod
    def run_animation_validation(tab_params):
        """Updates and runs animation validation"""
        _DataHandler.update_anim_validation_settings(tab_params)
        BackEndCommands.run_validation(animation_validation=True)

        return

    @staticmethod
    def update_anim_validation_settings(tab_params):
        """Packs variables for update"""

        anim_settings = [tab_params["attributes"], tab_params["min_frame"], tab_params["max_frame"]]
        BackEndCommands.update_settings(anim_settings=anim_settings)

        return

    @staticmethod
    def run_character_validation(tab_params):
        """Updates and runs validation"""

        _DataHandler.update_char_validation_settings(tab_params)
        BackEndCommands.run_validation(character_validation=True)

        return

    @staticmethod
    def update_char_validation_settings(tab_params):
        """Packs variables for update"""
        char_settings = [tab_params["valid_materials"], tab_params["min_frame"], tab_params["max_frame"]]
        BackEndCommands.update_settings(character_settings=char_settings)

        return

    @staticmethod
    def run_prop_validation(tab_params):
        """Updates and runs validation"""
        _DataHandler.update_prop_validation_settings(tab_params)
        BackEndCommands.run_validation(prop_validation=True)

        return

    @staticmethod
    def update_prop_validation_settings(tab_params):
        """Packs variables for update"""
        prop_settings = [tab_params["valid_materials"], tab_params["min_frame"], tab_params["max_frame"],
                         tab_params["collision_prefix"]]
        BackEndCommands.update_settings(prop_settings=prop_settings)

        return

    @staticmethod
    def run_all_validation_groups():
        """Runs all validation groups in a single call"""
        BackEndCommands.run_validation(character_validation=True, animation_validation=True, prop_validation=True)
