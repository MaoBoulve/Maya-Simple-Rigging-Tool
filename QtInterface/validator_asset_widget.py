# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.


"""
Validator asset group tagging widget. Connects objects selected by user in the Maya scene to the metadata group
of the dropdown window. Updates widget via re-queries into the state of the metadata asset group.
"""


from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
from qt_utils import QtMayaUtils, QtMetadataUtils


class AssetTaggingWidget(WidgetTemplate.QtMayaWidgetWindow):
    """
    Qt Asset Widget class.

    Qt Classes used:
    -QPushButton
    -QlistWidget
    -QComboBox
    """

    def __init__(self):

        self.btn_add_to_group = None
        self.btn_remove_from_group = None
        self.validation_group_dropdown = None

        self.asset_list = None
        self.btn_close = None
        self.btn_open_settings = None

        super().__init__(filepath=__file__, window_title="Validator Asset Tagging",
                         window_object_name="validatorTaggingWindow")

        return

    def _collect_ui_elements(self):
        self.btn_close = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_close')
        self.btn_open_settings = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_open_settings')
        self.asset_list = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'asset_list')

        self.validation_group_dropdown = self.QWidget_instance.findChild(QtWidgets.QComboBox, 'validation_groups_dropdown')
        self.btn_add_to_group = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_add_to_group')
        self.btn_remove_from_group = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_remove_from_group')

        return

    def _initialize_ui_element_states(self):
        self.__initialize_validation_group_dropdown()

        return

    def __initialize_validation_group_dropdown(self):
        """
        Initialize dropdown list to validation group names
        """

        # gets list of names
        maya_node_names = _DataHandler.get_validator_group_names()

        # appends after conversion
        for node in maya_node_names:
            self.validation_group_dropdown.addItem(str(node))

        # first entry in names is what dropdown list starts with
        self.__populate_asset_list_with_validation_group(maya_node_names[0])

        return

    def __populate_asset_list_with_validation_group(self, group_node_name):
        """
        Gets maya object names of current validation group and appends names to list widget
        """

        # clears prior list
        self.asset_list.clear()

        # gets list of maya objects from metadata
        assets_to_populate = _DataHandler.get_validation_group_assets(group_node_name)

        # appends after conversion
        for single_asset in assets_to_populate:
            self.asset_list.addItem(str(single_asset))

        return

    def _create_ui_connections_to_class_functions(self):
        """
        Connects UI events to python methods
        """

        self.btn_close.clicked.connect(self.__on_btn_close_clicked)
        self.btn_open_settings.clicked.connect(self.__on_btn_open_settings_clicked)

        self.asset_list.currentTextChanged.connect(self.__on_asset_list_current_text_changed)

        self.validation_group_dropdown.currentTextChanged.connect(self.__on_dropdown_current_text_changed)

        self.btn_add_to_group.clicked.connect(self.__on_btn_add_clicked)
        self.btn_remove_from_group.clicked.connect(self.__on_btn_remove_clicked)

        return

    def __on_btn_close_clicked(self):
        """
        Closes window on click event
        """

        self._close_window()
        return

    @staticmethod
    def __on_btn_open_settings_clicked():
        """
        Opens settings widget
        """
        _DataHandler.open_settings()

        return

    @staticmethod
    def __on_asset_list_current_text_changed(new_text):
        """
        If new_text has text, select the corresponding maya object
        """
        
        _DataHandler.select_maya_object_by_name(new_text)

        return

    def __on_dropdown_current_text_changed(self, new_dropdown_group_name):
        """
        When dropdown text changed, set asset list to validation group
        """

        self.__populate_asset_list_with_validation_group(new_dropdown_group_name)

        return

    def __on_btn_add_clicked(self):
        """
        If a maya object is selected, attempts to add it to the current dropdown validation maya node

        If successful, updates asset list UI
        """

        validation_group_name = self.validation_group_dropdown.currentText()
        group_change = _DataHandler.connect_objects_selected_in_maya_to_validation_group(
            validation_group_name)

        if group_change:
            self.__populate_asset_list_with_validation_group(validation_group_name)

        return

    def __on_btn_remove_clicked(self):
        """
        If one of the asset list items is selected, attempts to disconnect it from the validation maya node

        If successful, calls update to asset list UI
        """

        selected_item_as_widget = self.asset_list.currentItem()
        if selected_item_as_widget is None:
            return

        selected_item_name = selected_item_as_widget.text()

        validation_group_name = self.validation_group_dropdown.currentText()

        group_change = _DataHandler.remove_object_from_validation_group(selected_item_name,
                                                                        validation_group_name)

        if group_change:
            self.__populate_asset_list_with_validation_group(validation_group_name)

        return


class _DataHandler:
    """
    Data Handler class to isolate dependency on Util classes away from Widget class
    """

    @staticmethod
    def open_settings():
        """
        Front End call to open validator settings widget
        """
        from validator_commands import FrontEndCommands
        FrontEndCommands.open_validator_settings_widget()
        return

    @staticmethod
    def get_validator_group_names():
        """
        Gets names of all validator group names, converts to title strings and sets dropdown options to list
        """
        group_names = QtMetadataUtils.get_validator_group_names()

        for i in range(len(group_names)):
            group_names[i] = _DataHandler.__convert_maya_node_name_to_readable_name(group_names[i])

        return group_names

    @staticmethod
    def __convert_maya_node_name_to_readable_name(maya_name='example_node_name'):
        """
        Converts node name structure to title string with spacing
        """
        readable_name = maya_name.replace('_', ' ')
        readable_name = readable_name.title()

        return readable_name

    @staticmethod
    def __convert_readable_name_back_to_maya_node_name(readable_name='Example Node Name'):
        """
        Converts title string to node name
        """
        maya_name = readable_name.replace(' ', '_')
        maya_name = maya_name.lower()

        return maya_name

    @staticmethod
    def get_validation_group_assets(widget_group_name):
        """
        Converts widget group name to maya node and gets assets
        """
        maya_node_name = _DataHandler.__convert_readable_name_back_to_maya_node_name(widget_group_name)
        return QtMetadataUtils.get_validation_group_assets(maya_node_name)

    @staticmethod
    def select_maya_object_by_name(object_name):
        """
        Selects maya object matching name. Object can be invalid if deleted outside widget UI updates
        """
        try:
            QtMayaUtils.select_object_by_name(object_name)

        except TypeError:
            return
        except ValueError:
            return

    @staticmethod
    def connect_objects_selected_in_maya_to_validation_group(validation_group_maya_name):
        """
        Connects the items to the pynode
        """

        maya_node_name = _DataHandler.__convert_readable_name_back_to_maya_node_name(validation_group_maya_name)
        is_success = QtMetadataUtils.connect_selected_maya_objects_to_validation_group(maya_node_name)

        return is_success

    @staticmethod
    def remove_object_from_validation_group(object_maya_name, validation_group_maya_name):
        """
        If object is valid, removes object from validation group.

        Object can be invalid if maya or user deletes object outside of widget update calls,
        in which case return True to have UI update to current metadata node state.
        """
        try:
            object_to_remove = QtMayaUtils.get_maya_object_by_name(object_maya_name)

            maya_node_name = _DataHandler.__convert_readable_name_back_to_maya_node_name(validation_group_maya_name)

            is_success = QtMetadataUtils.disconnect_objects_from_validation_group(object_to_remove, maya_node_name)
            QtMayaUtils.deselect_object_by_name(object_maya_name)

        except TypeError:
            return True
        except ValueError:
            return True

        return is_success
