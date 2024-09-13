# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Main widget module
"""

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
from weight_painting_tab_widget import WeightPaintingTabWidget
from skeleton_tab_widget import SkeletonTabWidget
from rig_control_tab_widget import RigControlTabWidget

import output_system_commands

class SimpleRigToolWindowWidget(WidgetTemplate.QtMayaWidgetWindow):
    """
    Simple rig tool widget. Contains following nested QWidgets:

    - SkeletonTabWidget
    - RigControlTabWidget
    - WeightPaintingTabWidget
    """

    def __init__(self):

        self.btn_close = None
        self.weight_paint_tab = None

        super().__init__(filepath=__file__, window_title="Simple Rigging Tool",
                         window_object_name="simpleRigToolWindow")

    def _collect_ui_elements(self):

        self.btn_close = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_close')
        self.list_output = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_output')

        # individual tabs of QTabWidgets are QWidgets
        weight_paint_tab = self.QWidget_instance.findChild(QtWidgets.QWidget, 'tab_weightPaint')
        self.weight_paint_tab = WeightPaintingTabWidget(weight_paint_tab, self)

        skeleton_tab = self.QWidget_instance.findChild(QtWidgets.QWidget, 'tab_skeleton')
        self.skeleton_tab = SkeletonTabWidget(skeleton_tab, self)

        rig_control_tab = self.QWidget_instance.findChild(QtWidgets.QWidget, 'tab_rigControl')
        self.rig_control_tab = RigControlTabWidget(rig_control_tab, self)

        return

    def _initialize_ui_element_states(self):
        _DataHandler.clear_current_output_queue()
        return

    def _create_ui_connections_to_class_functions(self):
        self.btn_close.clicked.connect(self._on_btn_close_clicked)
        return

    def _on_btn_close_clicked(self):
        self._close_window()
        return

    def populate_output_widget(self):
        """
        Populates output list widget with metadata node stored entries
        """

        output_queue = _DataHandler.retrieve_current_output_queue()

        for output_entry in output_queue:
            text_entry = output_entry[0]

            if text_entry != "":
                self.list_output.addItem(text_entry)

        _DataHandler.clear_current_output_queue()

        return

class _DataHandler:
    """
    Data handler class for connections and dependencies on Rigging module
    """

    @classmethod
    def retrieve_current_output_queue(cls):
        """
        Retrieves the current output queue
        :return: output_queue: list of string
        """
        output_queue = output_system_commands.get_current_output_log()
        return output_queue

    @classmethod
    def clear_current_output_queue(cls):
        """
        Clears current queue
        :return:
        """
        output_system_commands.clear_current_output_log()

        return

