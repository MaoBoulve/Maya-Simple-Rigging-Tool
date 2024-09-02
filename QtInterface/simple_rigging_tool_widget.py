# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

from PySide2 import QtWidgets

import qt_maya_widget_base as WidgetTemplate
import qt_maya_utils as QtMayaUtils
from qt_rigging_system_controls import WeightPaintingCommands, Output

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
        self.list_output = self.QWidget_instance.findChild(QtWidgets.QListWidget, 'list_output')

        # individual tabs of QTabWidgets are QWidgets
        weight_paint_tab_widget = self.QWidget_instance.findChild(QtWidgets.QWidget, 'tab_weightPaint')
        self.weight_paint_tab = _WeightPaintingTabWidget(weight_paint_tab_widget, self)

        return

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        self.btn_close.clicked.connect(self._on_btn_close_clicked)

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

        return
class _WeightPaintingTabWidget(WidgetTemplate.QtMayaNestedWidget):


    def __init__(self, widget_container, parent_window_instance):
        self.parent_window = parent_window_instance

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

        joint, mesh, vertex = _DataHandler.get_current_weight_paint_settings()

        if joint:
            self._update_current_weight_paint_joint(joint)

        if mesh:
            self._update_current_mesh(mesh)

        if vertex:
            self._update_current_vertex(vertex)

        self._check_to_enable_weight_paint_buttons()

        return



    def _create_ui_connections_to_class_functions(self):
        self.btn_assignWeightPaintJoint.clicked.connect(self._on_btn_assignWeightPaintJoint_clicked)
        self.btn_assignWeightMesh.clicked.connect(self._on_btn_assignWeightMesh_clicked)
        self.btn_applyMeshPaint.clicked.connect(self._on_btn_applyMeshPaint_clicked)
        self.btn_assignWeightVertex.clicked.connect(self._on_btn_assignWeightVertex_clicked)
        self.btn_applyVertexPaint.clicked.connect(self._on_btn_applyVertexPaint_clicked)

        self.list_weightJoint.itemClicked.connect(self._on_jointList_item_clicked)
        self.list_meshPaint.itemClicked.connect(self._on_meshList_item_clicked)
        self.list_vertexPaint.itemClicked.connect(self._on_vertexList_item_clicked)

        return

    def _on_btn_assignWeightPaintJoint_clicked(self):
        self._assign_selected_joint_as_weight_paint_source()
        self._call_output_update()
        return

    def _assign_selected_joint_as_weight_paint_source(self):
        """
        Checks current selected maya object for single joint. If valid, sets as new joint in back end and in widget
        """

        is_success, new_joint = _DataHandler.update_weight_paint_joint()

        if is_success:
            self._update_current_weight_paint_joint(new_joint)
            self._check_to_enable_weight_paint_buttons()

        return

    def _update_current_weight_paint_joint(self, new_joint_name):
        """
        Removes prior item, adds new item
        :param new_joint_name: string entry
        """

        self.list_weightJoint.takeItem(0)
        self.list_weightJoint.addItem(new_joint_name)

        return

    def _check_to_enable_weight_paint_buttons(self):
        mesh_valid = _DataHandler.check_is_mesh_paint_parameters_set()

        if mesh_valid:
            self.btn_applyMeshPaint.setEnabled(True)

        vertex_valid = _DataHandler.check_is_vertex_paint_parameters_set()

        if vertex_valid:
            self.btn_applyVertexPaint.setEnabled(True)

        return

    def _call_output_update(self):
        """
        Calls SimpleRigtoolWindowWidget function for populate output widget
        """
        self.parent_window.populate_output_widget()
        return

    def _on_btn_assignWeightMesh_clicked(self):
        self._assign_selected_mesh_as_weight_paint_target()
        self._call_output_update()
        return

    def _assign_selected_mesh_as_weight_paint_target(self):


        is_success, new_mesh = _DataHandler.update_mesh_to_paint()

        if is_success:
            self._update_current_mesh(new_mesh)
            self._check_to_enable_weight_paint_buttons()

        return

    def _update_current_mesh(self, new_mesh_name):
        """
        Removes prior item, adds new item
        :param new_mesh_name: string entry
        """

        self.list_meshPaint.takeItem(0)
        self.list_meshPaint.addItem(new_mesh_name)

        return

    def _on_btn_applyMeshPaint_clicked(self):
        self._apply_new_mesh_weight_paint()
        self._call_output_update()
        return

    def _apply_new_mesh_weight_paint(self):
        """
        Gets current spinbox value for mesh weight paint, calls back end system to apply mesh weight paint
        """
        weight_paint_value = self.spinBox_meshWeight.value()
        _DataHandler.apply_mesh_weight_paint(weight_paint_value)

        return

    def _on_btn_assignWeightVertex_clicked(self):
        self._assign_selected_vertex_as_weight_paint_target()
        self._call_output_update()
        return

    def _assign_selected_vertex_as_weight_paint_target(self):

        is_success, vertex_count = _DataHandler.update_vertex_to_paint()

        if is_success:
            self._update_current_vertex(vertex_count)
            self._check_to_enable_weight_paint_buttons()

        return

    def _update_current_vertex(self, new_vertex_count):
        """
        Removes prior item, adds new item
        :param new_vertex_count: int count
        """

        self.list_vertexPaint.takeItem(0)
        self.list_vertexPaint.addItem(f"{new_vertex_count} Vertex selected")

        return

    def _on_btn_applyVertexPaint_clicked(self):
        self._apply_new_vertex_weight_paint()
        self._call_output_update()
        return

    def _apply_new_vertex_weight_paint(self):
        """
        Gets current spinbox value for mesh weight paint, calls back end system to apply mesh weight paint
        """

        weight_paint_value = self.spinBox_vertexWeight.value()
        _DataHandler.apply_vertex_weight_paint(weight_paint_value)

        pass

    @staticmethod
    def _on_jointList_item_clicked(item_clicked):
        # signal emits a QListWidgetItem object
        item_text = item_clicked.text()

        if item_text == '--':
            return

        _DataHandler.select_current_joint()

        return

    @staticmethod
    def _on_meshList_item_clicked(item_clicked):

        item_text = item_clicked.text()

        if item_text == '--':
            return

        _DataHandler.select_current_mesh()
        return

    @staticmethod
    def _on_vertexList_item_clicked(item_clicked):

        item_text = item_clicked.text()

        if item_text == '--':
            return

        _DataHandler.select_current_vertex()

        return

class _DataHandler:
    """
    Data handler class for connections and dependencies on Rigging module
    """


    @classmethod
    def update_weight_paint_joint(cls):

        new_joint = QtMayaUtils.get_user_selected_maya_objects()
        is_success = WeightPaintingCommands.set_weight_paint_joint(new_joint)

        if is_success:
            new_joint_name = str(new_joint[0])

        else:
            _DataHandler.append_to_output_queue("-Selected object is not a Joint")
            new_joint_name = ""

        return is_success, new_joint_name

    @classmethod
    def update_mesh_to_paint(cls):


        new_mesh = QtMayaUtils.get_user_selected_maya_objects()
        is_success = WeightPaintingCommands.set_mesh_to_paint(new_mesh)

        if is_success:
            new_mesh_name = str(new_mesh[0])

        else:

            _DataHandler.append_to_output_queue("-Selected object is not a Mesh")
            new_mesh_name = ""

        return is_success, new_mesh_name

    @classmethod
    def update_vertex_to_paint(cls):

        new_vertex_list = QtMayaUtils.get_user_selected_maya_objects()
        is_success = WeightPaintingCommands.set_vertex_list_to_paint(new_vertex_list)

        if is_success:
            vertex_count = QtMayaUtils.count_distinct_vertex_from_sliced_list(new_vertex_list)

        else:
            _DataHandler.append_to_output_queue("-Selected object is not a Vertex or multiple vertex from a single mesh")

            vertex_count = -1

        return is_success, vertex_count

    @classmethod
    def apply_mesh_weight_paint(cls, weight_paint_value):
        WeightPaintingCommands.apply_mesh_weight_paint(weight_paint_value)
        return

    @classmethod
    def apply_vertex_weight_paint(cls, weight_paint_value):
        WeightPaintingCommands.apply_vertex_weight_paint(weight_paint_value)
        return

    @classmethod
    def select_current_joint(cls):
        object_to_select = WeightPaintingCommands.get_current_weight_paint_joint()
        QtMayaUtils.select_maya_object(object_to_select)

        return

    @classmethod
    def select_current_mesh(cls):
        object_to_select = WeightPaintingCommands.get_current_weight_paint_mesh()
        QtMayaUtils.select_maya_object(object_to_select)

        return

    @classmethod
    def select_current_vertex(cls):
        object_to_select = WeightPaintingCommands.get_current_weight_paint_vertex_list()
        QtMayaUtils.select_maya_object(object_to_select)

        return

    @classmethod
    def check_is_mesh_paint_parameters_set(cls):
        is_valid = True

        joint = WeightPaintingCommands.get_current_weight_paint_joint()
        mesh = WeightPaintingCommands.get_current_weight_paint_mesh()

        if joint is None or mesh is None:
            is_valid = False

        return is_valid

    @classmethod
    def check_is_vertex_paint_parameters_set(cls):
        is_valid = True

        joint = WeightPaintingCommands.get_current_weight_paint_joint()
        vertex = WeightPaintingCommands.get_current_weight_paint_vertex_list()

        if joint is None or vertex is None:
            is_valid = False

        return is_valid

    @classmethod
    def retrieve_current_output_queue(cls):
        output_queue = Output.get_current_output_queue()
        Output.clear_current_output_queue()
        return output_queue

    @classmethod
    def append_to_output_queue(cls, entry):
        Output.append_to_output_queue(entry, "")
        return

    @classmethod
    def get_current_weight_paint_settings(cls):
        joint = str(WeightPaintingCommands.get_current_weight_paint_joint())
        mesh = str(WeightPaintingCommands.get_current_weight_paint_mesh())

        vertex = WeightPaintingCommands.get_current_weight_paint_vertex_list()
        vertex = QtMayaUtils.count_distinct_vertex_from_sliced_list(vertex)
        return joint, mesh, vertex