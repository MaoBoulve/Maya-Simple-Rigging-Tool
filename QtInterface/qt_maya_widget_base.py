# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.


"""
Qt Maya Widget template for consistent initialization and control structure
"""
from abc import abstractmethod
import os
from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets


def _get_maya_window():
    """
    Gets Maya window for use by Qt Widget
    """
    from maya import OpenMayaUI
    ptr = OpenMayaUI.MQtUtil.mainWindow()

    from shiboken2 import wrapInstance
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class QtMayaWidget(QtWidgets.QDialog):
    """
    Qt Widget template base. Defines abstract methods for connecting to Maya & Python

    __init__ calls abstract methods in order:
        1. _init_ui_file
        2. _collect_ui_elements
        3. _initialize_ui_element_states
        4. _create_ui_connections_to_class_functions

    super().__init__() must be called in deriving classes if __init__ is overridden
    """

    #TODO: declare QWidget instance as an abstract property
    # https://stackoverflow.com/questions/2736255/abstract-attributes-in-python

    def __init__(self, parent=_get_maya_window()):
        """
        Maya Widget init call
        """

        super(QtMayaWidget, self).__init__(parent)

        self._QWidget_instance = None # QtWidget_instance is QWidget container holding all buttons, text, etc.
        self._collect_ui_elements()
        self._initialize_ui_element_states()
        self._create_ui_connections_to_class_functions()

        return


    @abstractmethod
    def _collect_ui_elements(self):
        """
        Abstract method for setting ui elements to python variables for use
        """
        print("-- Deriving class needs to override '_collect_ui_elements ")

        return

    @abstractmethod
    def _initialize_ui_element_states(self):
        """
        Abstract method to initialize UI state of widget
        """
        print("-- Deriving class needs to override '_initialize_ui_element_states ")

        return

    @abstractmethod
    def _create_ui_connections_to_class_functions(self):
        """
        Abstract method to connect QWidget signals to python methods
        """
        print("-- Deriving class needs to override '_create_ui_connections_to_class_functions ")

        return


class QtMayaWidgetWindow(QtMayaWidget):
    """
    Qt Window Widget base class.
    Loads Qt .ui files assuming python file name matches Qt file and placed in same directory

    Deriving classes should override:
    -collect_ui_elements.
    -set_ui_element_states.
    -create_ui_connections_to_class_functions.

    Deriving classes need to call super().__init__(filename=__file__) in __init__ (after any variable declarations)
    """

    def __init__(self, filepath=__file__, window_title="Sandbox Window", window_object_name="sandboxWindow"):
        """
        Init call initializing the file name to look for, window name parameters
        :param filepath: full filepath to maya file, used for finding Qt file
        :param window_title: window title displayed in Maya
        :param window_object_name: window name for python indexing
        """
        self.filepath = filepath

        self.window_title = window_title
        self.window_object_name = window_object_name
        self._init_ui_file()

        super().__init__()

        self.__clear_previous_windows()

        return

    def _init_ui_file(self):
        """
        Loading Qt Widget file via local directory search. Initializes widget window with instance variables.
        """

        # Load UI
        file_full_path = os.path.abspath(self.filepath)
        # Grab the .ui file that matches this python file name in the same directory
        ui_path = file_full_path.replace('.py', '.ui')

        # Read a pyqt .ui file
        qt_ui_file = QtCore.QFile(ui_path)
        qt_ui_file.open(QtCore.QFile.ReadOnly)

        # Load the file and store in instance variable
        loader = QtUiTools.QUiLoader()
        self.QWidget_instance = loader.load(qt_ui_file)

        self.set_QWidget_instance(loader.load(qt_ui_file))

        # Set the object name
        self.setObjectName(self.window_object_name)
        # Set the title on the Parent Widget
        self.setWindowTitle(self.window_title)
        # Set the UI file parent to the QDialog ExampleWindow root
        self.QWidget_instance.setParent(self)

        qt_ui_file.close()

        return

    @abstractmethod
    def _collect_ui_elements(self):
        print("Need to override collect_ui_elements")
        return

    @abstractmethod
    def _initialize_ui_element_states(self):
        print("Need to override initialize_ui_element_states")
        return

    @abstractmethod
    def _create_ui_connections_to_class_functions(self):
        print("Need to override create_ui_connections_to_class_functions")
        return

    def __clear_previous_windows(self):
        """
        Looks for any prior instance of this window and closes
        """

        # Maya uses this so it should always return True?
        if QtWidgets.QApplication.instance():
            # ID any current instances of tool and destroy
            for win in (QtWidgets.QApplication.allWindows()):

                if self.window_object_name in win.objectName():  # if object name matches, destroy the matching window
                    win.destroy()

        else:
            print("Application instance invalid, previous windows not closed")

        return

    def _close_window(self):
        """
        Closes Qt widget
        """
        self.destroy()

        return


class QtMayaNestedWidget(QtMayaWidget):
    """
    Qt Maya widget class for widgets already loaded in the initial .ui instantiation (tool box, tab widget, stacked widget)

    Instances are created with reference to QWidget

    Deriving classes should override:
    -collect_ui_elements.
    -set_ui_element_states.
    -create_ui_connections_to_class_functions.
    """

    def __init__(self, tab_widget_parent):
        """
        Init call
        """
        self.widget_parent = tab_widget_parent
        super().__init__()
        return
