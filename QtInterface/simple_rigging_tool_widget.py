# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
from qt_utils import QtMayaUtils, QtMetadataUtils

class SimpleRigToolWindowWidget(WidgetTemplate.QtMayaWidgetWindow):
    """
    Simple rig tool widget. Contains following nested QWidgets:

    - WeightPaintingTabWidget
    """

    def __init__(self):

        self.btn_close = None
        self.weight_paint_tab = None

        super().__init__(filepath=__file__, window_title="Simple Rigging Tool",
                         window_object_name="simpleRigToolWindow")

    def _collect_ui_elements(self):

        self.btn_close = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_close')

        # individual tabs of QTabWidgets are QWidgets
        weight_paint_tab_widget = self.QWidget_instance.findChild(QtWidgets.QWidget, 'tab_weightPaint')
        self.weight_paint_tab = _WeightPaintingTabWidget(weight_paint_tab_widget)

        return

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        self.btn_close.clicked.connect(self._on_btn_close_clicked)

    def _on_btn_close_clicked(self):
        self._close_window()
        return

class _WeightPaintingTabWidget(WidgetTemplate.QtMayaNestedWidget):


    def __init__(self, widget_container):
        super().__init__(widget_container)

    def _collect_ui_elements(self):
        self.btn_assignWeightPaintJoint = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_assignWeightPaintJoint')
        self.btn_assignWeightMesh = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_assignWeightMesh')
        self.btn_applyMeshPaint = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_applyMeshPaint')
        self.btn_assignWeightVertex = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_assignWeightVertex')
        self.btn_applyVertexPaint = self.QWidget_instance.findChild(QtWidgets.QPushButton, 'btn_applyVertexPaint')

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        self.btn_assignWeightPaintJoint.clicked.connect(self._on_btn_assignWeightPaintJoint_clicked)
        self.btn_assignWeightMesh.clicked.connect(self._on_btn_assignWeightMesh_clicked)
        self.btn_applyMeshPaint.clicked.connect(self._on_btn_applyMeshPaint_clicked)
        self.btn_assignWeightVertex.clicked.connect(self._on_btn_assignWeightVertex_clicked)
        self.btn_applyVertexPaint.clicked.connect(self._on_btn_applyVertexPaint_clicked)

    def _on_btn_assignWeightPaintJoint_clicked(self):
        print("_on_btn_assignWeightPaintJoint_clicked")

    def _on_btn_assignWeightMesh_clicked(self):
        print("_on_btn_assignWeightMesh_clicked")

    def _on_btn_applyMeshPaint_clicked(self):
        print("_on_btn_applyMeshPaint_clicked")

    def _on_btn_assignWeightVertex_clicked(self):
        print("_on_btn_assignWeightVertex_clicked")

    def _on_btn_applyVertexPaint_clicked(self):
        print("_on_btn_applyVertexPaint_clicked")