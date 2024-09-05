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

def _convert_list_to_attribute_string(string_list):
    """
    Converts string list to single string for maya node attributes. Delimiter is ',' character.
    """
    single_string = ','.join(string_list)

    return single_string


def _parse_attribute_string_to_list(single_string):
    """
    Converts single string to string list. Assumes delimiter is ',' character.
    """
    string_list = single_string.split(',')

    return string_list

def _check_and_convert_null_set_input(set_value, value_type='string'):
    """
    Check and converts None/null to values maya will accept for nodes. Ideally never used in any user parameters.

    Attribute null values:
    'NONE', -999, -333.333

    :param set_value: Value to check
    :param value_type: 'string', 'short', 'double'
    """
    if set_value is None or len([set_value]) < 1:
        if value_type == 'string':
            set_value = 'NONE'

        if value_type == 'short':
            set_value = -999

        if value_type == 'double':
            set_value = -333.333

    return set_value


def _check_and_convert_null_get_input(get_value):
    """
    Checks and converts maya attribute null values to None python values.

    Attribute null values:
    'NONE', -999, -333.333
    """
    if get_value == 'NONE':
        get_value = None

    if get_value == -999:
        get_value = None

    if get_value == -333.333:
        get_value = None

    return get_value

class WeightPaintingMetadataNode(DependentNode):
    """
    Weight painting metadata node. Stores current settings for joint/mesh/vertex in weight painting tab
    """
    dependent_node = Core
    maya_node_name = 'weight_painting'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         joint=('', 'string'),
                         mesh=('', 'string'),
                         vertex=('', 'string'))
        return

    @classmethod
    def __get_weight_painting_maya_node(cls):
        maya_get = pm.ls('weight_painting')

        if maya_get:
            return maya_get[0]
        else:
            return None

    @classmethod
    def __get_weight_painting_metadata_instance(cls):
        maya_node = cls.__get_weight_painting_maya_node()
        metadata_instance = WeightPaintingMetadataNode(node=maya_node)

        return metadata_instance

    @classmethod
    def set_new_weight_paint_joint(cls, joint_name):
        class_instance = cls.__get_weight_painting_metadata_instance()
        WeightPaintingMetadataNode.set(class_instance, 'joint', joint_name)

        return

    @classmethod
    def get_weight_paint_joint(cls):
        class_instance = cls.__get_weight_painting_metadata_instance()
        joint_name = WeightPaintingMetadataNode.get(class_instance, 'joint')

        joint_object = pm.ls(joint_name)

        if joint_object:
            return joint_object[0]
        else:
            return None


    @classmethod
    def set_new_mesh(cls, mesh_name):
        class_instance = cls.__get_weight_painting_metadata_instance()
        WeightPaintingMetadataNode.set(class_instance, 'mesh', mesh_name)

        return

    @classmethod
    def get_mesh(cls):
        class_instance = cls.__get_weight_painting_metadata_instance()
        mesh_name = WeightPaintingMetadataNode.get(class_instance, 'mesh')

        mesh_object = pm.ls(mesh_name)

        if mesh_object:
            return mesh_object[0]
        else:
            return None


    @classmethod
    def set_new_vertex_list(cls, vertex_list):
        class_instance = cls.__get_weight_painting_metadata_instance()

        vertex_list = [str(x) for x in vertex_list]

        list_as_string = _convert_list_to_attribute_string(vertex_list)

        WeightPaintingMetadataNode.set(class_instance, 'vertex', list_as_string)

        return

    @classmethod
    def get_vertex_list(cls):
        class_instance = cls.__get_weight_painting_metadata_instance()

        long_string = WeightPaintingMetadataNode.get(class_instance, 'vertex')
        vertex_list = _parse_attribute_string_to_list(long_string)

        # convert from string to maya object
        vertex_list = pm.ls(vertex_list)

        return vertex_list

class RigControllersMetadataNode(DependentNode):
    """
    Output Log public class for handling validation result display
    """
    dependent_node = Core
    maya_node_name = 'rig_control'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         joint=('', 'string'),
                         mesh=('', 'string'),
                         vertex=('', 'string'))
        return


class OutputLog(DependentNode):
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
        output_maya_node = OutputLog.__get_output_maya_node()
        output_node = OutputLog(node=output_maya_node)

        OutputLog.set(output_node, 'output_log', '')
        OutputLog.set(output_node, 'target_object_name', '')

        return

    @classmethod
    def add_to_output_log(cls, log_entry, target_object_name):
        output_maya_node = OutputLog.__get_output_maya_node()
        output_node = OutputLog(node=output_maya_node)

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
        current_string = OutputLog.get(output_node, attribute)

        if current_string == '':
            new_attrib_string = new_string

        else:
            new_attrib_string = current_string + "`" + new_string

        OutputLog.set(output_node, attribute, new_attrib_string)
        return

    @classmethod
    def get_output_log(cls):
        """

        :return: Returns 2 lists of following outputs

        [output_log]

        [target_object_name]
        """
        output_maya_node = pm.ls('output_log')

        if output_maya_node:
            output_maya_node = output_maya_node[0]
        else:
            output_maya_node = None

        output_node = OutputLog(node=output_maya_node)

        output_log = OutputLog.__get_output_node_attribute_value_as_list(output_node, attribute='output_log')
        target_object_name = OutputLog.__get_output_node_attribute_value_as_list(output_node,
                                                                                 attribute='target_object_name')

        return output_log, target_object_name

    @staticmethod
    def __get_output_node_attribute_value_as_list(output_node, attribute='output_log'):
        long_string = OutputLog.get(output_node, attribute)
        value_as_list = OutputLog.__parse_string_to_list(long_string)

        return value_as_list

