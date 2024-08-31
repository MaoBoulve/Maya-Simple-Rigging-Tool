# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# network_core module copyright of Micah Zahm

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Module deriving from network_core for creating and accessing the rigging metadata system.
"""

import pymel.core as pm
from network_core import DependentNode, Core

class OutputQueueLog(DependentNode):
    """
    Output Log public class for handling validation result display
    """
    dependent_node = Core
    maya_node_name = 'output_log'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         output_log=('', 'string'),
                         target_object_name=('', 'string'))
        return

    @staticmethod
    def __parse_string_to_list(single_string):
        string_list = single_string.split('`')

        return string_list

    @classmethod
    def clear_output_log(cls):
        output_maya_node = OutputQueueLog.__get_output_maya_node()
        output_node = OutputQueueLog(node=output_maya_node)

        OutputQueueLog.set(output_node, 'output_log', '')
        OutputQueueLog.set(output_node, 'target_object_name', '')

        return

    @classmethod
    def add_to_output_log(cls, log_entry, target_object_name):
        output_maya_node = OutputQueueLog.__get_output_maya_node()
        output_node = OutputQueueLog(node=output_maya_node)

        cls.__append_to_output_node_attribute_strings(output_node, log_entry, attribute='output_log')
        cls.__append_to_output_node_attribute_strings(output_node, target_object_name, attribute='target_object_name')

        return

    @classmethod
    def __get_output_maya_node(cls):
        maya_get = pm.ls('output_log')

        if maya_get:
            return maya_get[0]
        else:
            return None

    @staticmethod
    def __append_to_output_node_attribute_strings(output_node, new_string, attribute='output_log'):
        current_string = OutputQueueLog.get(output_node, attribute)

        if current_string == '':
            new_attrib_string = new_string

        else:
            new_attrib_string = current_string + "`" + new_string

        OutputQueueLog.set(output_node, attribute, new_attrib_string)
        return

    @classmethod
    def get_output_log(cls):
        """

        :return: Returns 2 lists of following outputs

        [output_log]

        [target_object_name]
        """
        output_maya_node = pm.ls('output_log')[0]
        output_node = OutputQueueLog(node=output_maya_node)

        output_log = OutputQueueLog.__get_output_node_attribute_value_as_list(output_node, attribute='output_log')
        target_object_name = OutputQueueLog.__get_output_node_attribute_value_as_list(output_node,
                                                                                 attribute='target_object_name')

        return output_log, target_object_name

    @staticmethod
    def __get_output_node_attribute_value_as_list(output_node, attribute='output_log'):
        long_string = OutputQueueLog.get(output_node, attribute)
        value_as_list = OutputQueueLog.__parse_string_to_list(long_string)

        return value_as_list

