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

        self.weight_paint_tab = None

        super().__init__(filepath=__file__, window_title="Simple Rigging Tool",
                         window_object_name="simpleRigToolWindow")

    def _collect_ui_elements(self):
        pass

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        pass

class WeightPaintingTabWidget(WidgetTemplate.QtMayaNestedWidget):
    def _collect_ui_elements(self):
        pass

    def _initialize_ui_element_states(self):
        pass

    def _create_ui_connections_to_class_functions(self):
        pass