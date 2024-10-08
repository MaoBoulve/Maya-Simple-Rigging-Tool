# Simple Rigging Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

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

class SkeletonRigToolMetadataNode(DependentNode):
    """
    SkeletonRigging metadata node
    """
    dependent_node = Core
    maya_node_name = 'skeleton_rigging_tool'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         rig_root_joint=('', 'string'))
        return

    @classmethod
    def set_rig_root_joint(cls, root_joint):
        """
        Sets root joint metadata value
        :param root_joint: string
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        SkeletonRigToolMetadataNode.set(class_instance, 'rig_root_joint', root_joint)

        return

    @classmethod
    def get_rig_root_joint(cls):
        """
        Gets rig root joint
        :return: root_joint - maya object
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        root_joint = SkeletonRigToolMetadataNode.get(class_instance, 'rig_root_joint')

        root_joint = pm.ls(root_joint)

        if root_joint:
            return root_joint[0]
        else:
            return None

class RigControllersMetadataNode(DependentNode):
    """
    Rig Control metadata node
    """
    dependent_node = Core
    maya_node_name = 'rig_control'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         target_control_shape=('', 'string'),
                         target_joint=('', 'string'))
        return


    @classmethod
    def set_target_control_shape(cls, control_shape):
        """
        Sets target control metadata value
        :param control_shape: string
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        RigControllersMetadataNode.set(class_instance, 'target_control_shape', control_shape)

        return

    @classmethod
    def get_target_control_shape(cls):
        """
        Gets target control shape
        :return: target_control - maya object
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        target_control_shape = RigControllersMetadataNode.get(class_instance, 'target_control_shape')

        target_control_shape = pm.ls(target_control_shape)

        if target_control_shape:
            return target_control_shape[0]
        else:
            return None

    @classmethod
    def set_target_joint(cls, target_joint):
        """
        Sets target joint metadata value
        :param target_joint: string
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        RigControllersMetadataNode.set(class_instance, 'target_joint', target_joint)

        return

    @classmethod
    def get_target_joint(cls):
        """
        Gets target root joint
        :return: target_joint - maya object
                """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        target_joint = RigControllersMetadataNode.get(class_instance, 'target_joint')

        target_joint = pm.ls(target_joint)

        if target_joint:
            return target_joint[0]
        else:
            return None

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
    def set_new_weight_paint_joint(cls, joint_name):
        """
        Sets joint name metadata value
        :param joint_name: string
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        WeightPaintingMetadataNode.set(class_instance, 'joint', joint_name)

        return

    @classmethod
    def get_weight_paint_joint(cls):
        """
        Gets weight paint joint
        :return: joint_object - maya object
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        joint_name = WeightPaintingMetadataNode.get(class_instance, 'joint')

        joint_object = pm.ls(joint_name)

        if joint_object:
            return joint_object[0]
        else:
            return None


    @classmethod
    def set_new_mesh(cls, mesh_name):
        """
        Sets mesh name metadata value
        :param mesh_name: string
                """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        WeightPaintingMetadataNode.set(class_instance, 'mesh', mesh_name)

        return

    @classmethod
    def get_mesh(cls):
        """
        Gets mesh metadata value
        :return: mesh_object - maya object
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()
        mesh_name = WeightPaintingMetadataNode.get(class_instance, 'mesh')

        mesh_object = pm.ls(mesh_name)

        if mesh_object:
            return mesh_object[0]
        else:
            return None


    @classmethod
    def set_new_vertex_list(cls, vertex_list):
        """
        Sets vertex list metadata value
        :param vertex_list: list of string
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()

        vertex_list = [str(x) for x in vertex_list]

        list_as_string = _convert_list_to_attribute_string(vertex_list)

        WeightPaintingMetadataNode.set(class_instance, 'vertex', list_as_string)

        return

    @classmethod
    def get_vertex_list(cls):
        """
        Gets vertex list metadata value
        :return: vertex_list - list of maya objects
        """
        class_instance = cls.get_metadata_class_instance_from_maya_node()

        long_string = WeightPaintingMetadataNode.get(class_instance, 'vertex')
        vertex_list = _parse_attribute_string_to_list(long_string)

        # convert from string to maya object
        vertex_list = pm.ls(vertex_list)

        return vertex_list




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
        """
        Converts an attribute string to readable python list
        :param single_string: attribute string, uses ` as separator value
        :return: string_list - list of string
        """
        string_list = single_string.split('`')

        return string_list

    @classmethod
    def clear_output_log(cls):
        """
        Clear output log values
        """
        output_maya_node = OutputLog.__get_output_maya_node()
        output_node = OutputLog(node=output_maya_node)

        OutputLog.set(output_node, 'output_log', '')
        OutputLog.set(output_node, 'target_object_name', '')

        return

    @classmethod
    def add_to_output_log(cls, log_entry, target_object_name):
        """
        Adds a value to output log
        :param log_entry: string
        :param target_object_name: string, maya object name
        """
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
        """
        Appends to output attribute to keep a persistent value
        :param output_node: maya node
        :param new_string: string
        :param attribute: string, name of attribute
        """
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

