# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.


"""
Output log widget for displaying results of validation tasks. Allows user to select related maya object tied to each
output entry. Has functionality for color coordinating entries but Maya appears to not accept Qt color brush settings.
"""
import qt_maya_widget_base as WidgetTemplate
from PySide2 import QtWidgets, QtCore

from qt_utils import QtMayaUtils


class OutputWidget(WidgetTemplate.QtMayaWidgetWindow):
    """
    Qt Output Widget for displaying log of entries from metadata node

    Qt Classes used:
    -QPushButton
    -QlistWidget
    """

    def __init__(self):

        self.btn_rerun = None
        self.output_list = None
        self.btn_close = None

        super().__init__(filepath=__file__, window_title="Validator Output Log",
                         window_object_name="validatorOutputWindow")

        return

    def _collect_ui_elements(self):
        self.btn_close = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_close')
        self.btn_rerun = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_rerun')

        self.output_list = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'output_list')

        return

    def _initialize_ui_element_states(self):
        self.__populate_output_log()

        return

    def __populate_output_log(self):
        """
        Populates list widget with current output log string list.
        """
        _DataHandler.pull_current_output_log_list()

        for list_index in range(_DataHandler.list_length):
            output_entry = _DataHandler.output_log[list_index]

            self.__add_item_to_output_widget(output_entry)

            self.__align_item_on_key(list_index)

        return

    def __add_item_to_output_widget(self, entry):
        """
        Adding item to list widget
        """
        entry = str(entry)
        self.output_list.addItem(entry)

        return

    def __align_item_on_key(self, list_index):
        """
        Aligning task start/end entries to center
        """

        item_widget = self.output_list.item(list_index)
        entry_key = _DataHandler.entry_keys[list_index]

        if entry_key == 'task_start' or entry_key == 'task_success' or entry_key == 'task_failure':
            item_widget.setTextAlignment(QtCore.Qt.AlignCenter)

        return

    def _create_ui_connections_to_class_functions(self):
        self.btn_close.clicked.connect(self.__on_btn_close_clicked)
        self.btn_rerun.clicked.connect(self.__on_btn_rerun_clicked)

        self.output_list.itemClicked.connect(self.__on_output_list_item_clicked)

        return

    def __on_btn_close_clicked(self):
        """
        Closes window on click event
        """
        self._close_window()
        return

    @staticmethod
    def __on_btn_rerun_clicked():
        """
        Opens validation settings
        """
        _DataHandler.call_settings_widget_rerun_validation()

        return

    def __on_output_list_item_clicked(self, item_widget):
        """
        Selects maya object if available
        """

        item_index = self.output_list.row(item_widget)
        _DataHandler.select_item_index_maya_object(item_index)

        return


class _DataHandler:
    output_log = None
    entry_keys = None
    maya_object_name = None
    list_length = 0

    @classmethod
    def pull_current_output_log_list(cls):
        """
        Gets the current output log state and sets as class variables in _DataHandler for widget to use
        """
        from validator_network_nodes import OutputLog
        cls.output_log, cls.entry_keys, cls.maya_object_name = OutputLog.get_output_log()

        cls.list_length = len(cls.output_log)

        return

    @classmethod
    def select_item_index_maya_object(cls, item_index):
        """
        Selects maya object by name if available at the item index
        """
        object_name = _DataHandler.maya_object_name[item_index]

        if object_name == 'None' or object_name is None:
            return

        QtMayaUtils.select_object_by_name(object_name)

        return

    @staticmethod
    def call_settings_widget_rerun_validation():
        """
        Calls settings widget method to rerun validation
        """
        from validator_commands import FrontEndCommands
        FrontEndCommands.rerun_validation_on_current_validator_widget_settings()

        return
