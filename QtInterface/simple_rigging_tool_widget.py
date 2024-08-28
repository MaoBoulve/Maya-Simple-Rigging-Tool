# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
from qt_utils import QtMayaUtils, QtMetadataUtils
from rigging_commands import BackEndCommands

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

        self.list_weightJoint = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_weightJoint')
        self.list_meshPaint = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_meshPaint')
        self.list_vertexPaint = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_vertexPaint')

        self.spinBox_meshWeight = self.QWidget_instance.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_meshWeight')
        self.spinBox_vertexWeight = self.QWidget_instance.findChild(QtWidgets.QDoubleSpinBox, 'doubleSpinBox_vertexWeight')

        return


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
        self._assign_selected_joint_as_weight_paint_source()

    def _assign_selected_joint_as_weight_paint_source(self):
        # TODO: retrieve selected maya joint
        # TODO: validate is joint
        # TODO: pass to back end
        # TODO: update UI
        pass

    def _on_btn_assignWeightMesh_clicked(self):
        print("_on_btn_assignWeightMesh_clicked")
        self._assign_selected_mesh_as_weight_paint_target()

    def _assign_selected_mesh_as_weight_paint_target(self):
        # TODO: retrieve selected maya mesh
        # TODO: validate is mesh
        # TODO: pass to back end
        # TODO: update UI
        pass

    def _on_btn_applyMeshPaint_clicked(self):
        print("_on_btn_applyMeshPaint_clicked")
        self._apply_new_mesh_weight_paint()

    def _apply_new_mesh_weight_paint(self):
        # TODO: retrieve current spinBox value
        # TODO: call backend
        pass

    def _on_btn_assignWeightVertex_clicked(self):
        print("_on_btn_assignWeightVertex_clicked")
        self._assign_selected_vertex_as_weight_paint_target()

    def _assign_selected_vertex_as_weight_paint_target(self):
        # TODO: retrieve selected maya vertex
        # TODO: validate is from same object
        # TODO: pass to back end
        # TODO: update UI
        pass

    def _on_btn_applyVertexPaint_clicked(self):
        print("_on_btn_applyVertexPaint_clicked")
        self._apply_new_vertex_weight_paint()

    def _apply_new_vertex_weight_paint(self):
        # TODO: retrieve current spinBox value
        # TODO: call backend
        pass

class _DataHandler:
    """
    Data handler class for connections and dependencies on Rigging module
    """

    @classmethod
    def update_weight_paint_joint(cls, new_joint):
        BackEndCommands.WeightPainting.set_weight_paint_joint(new_joint)
        return

    @classmethod
    def update_mesh_to_paint(cls, new_mesh):
        BackEndCommands.WeightPainting.set_mesh_to_paint(new_mesh)
        return

    @classmethod
    def update_vertex_to_paint(cls, new_vertex_list):
        BackEndCommands.WeightPainting.set_vertex_list_to_paint(new_vertex_list)
        return

    @classmethod
    def apply_mesh_weight_paint(cls, weight_paint_value):
        BackEndCommands.WeightPainting.apply_mesh_weight_paint(weight_paint_value)
        return

    @classmethod
    def apply_vertex_weight_paint(cls, weight_paint_value):
        BackEndCommands.WeightPainting.apply_vertex_weight_paint(weight_paint_value)
        return