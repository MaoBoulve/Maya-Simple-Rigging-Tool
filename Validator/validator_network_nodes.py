# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# network_core module copyright of Micah Zahm

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Module deriving from network_core for creating and accessing the validator metadata system.
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


# type_dict = {str : "string", int : "short",
# float : 'double', bool : "bool", list : 'double3', pm.dt.Vector : 'double3'}

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


def _get_pynode_by_class(node_class=DependentNode):
    """
    Returns pynode matching class type argument. Checks if maya node associated with class type exists to initialize
    node attributes for persistent attributes

    :param node_class: class type, deriving from DependentNode
    :return: pynode class instance
    """
    maya_node_list = pm.ls(node_class.maya_node_name)

    if maya_node_list:
        maya_node = maya_node_list[0]
    else:
        maya_node = None

    pynode = node_class(node=maya_node)
    return pynode


class ValidationGroups(DependentNode):
    """
    Validation Groups public class for tagging assets as part of validation tasks.
    """
    dependent_node = Core
    maya_node_name = 'validation_groups'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace)

        return

    @staticmethod
    def __get_validation_group_dictionary():
        """
        Class itself cannot pull from class definitions so wrapping call in private function here
        Returns a dictionary with [key] - maya_node_name string, [value] - associated class

        Validated by pulling maya_node_name directly from class definitions
        """

        return _validation_groups_dict

    @staticmethod
    def get_name_of_all_group_maya_nodes():
        """
        Returns a string list of ALL validation group maya nodes
        """

        group_dict = ValidationGroups.__get_validation_group_dictionary()
        maya_node_names = list(group_dict.keys())

        return maya_node_names

    @staticmethod
    def get_group_assets(group_name='anim_validator'):
        """
        Returns group assets by dictionary map. If group name does not exist, returns an empty list

        Group names:
        'animation_group'

        'prop_group'

        'character_mesh_group'

        'character_skeleton_group'
        """

        group_dict = ValidationGroups.__get_validation_group_dictionary()

        try:
            group_class = group_dict[group_name]
            meta_node = _get_pynode_by_class(group_class)
            group_assets = meta_node.get_connections()
            return group_assets

        except KeyError:
            print(f"Invalid validation group name: {group_name}")
            return []

    @staticmethod
    def connect_assets_to_validation_group(asset_list, group_name='anim_validator'):
        """
        Connects assets to validation group. Returns a boolean if task was successful.

        :param asset_list: Pymel maya asset list
        :param group_name: Maya node name of validation group
        :return:
        """

        group_dict = ValidationGroups.__get_validation_group_dictionary()

        try:
            group_class = group_dict[group_name]
            meta_node = _get_pynode_by_class(group_class)

            meta_node.connect_nodes(asset_list)
            return True

        except KeyError:
            print(f"Invalid validation group name: {group_name}")
            return False

    @staticmethod
    def connect_selected_maya_objects_to_validation_group(group_name='anim_validator'):
        """
        If user has selected objects in Maya, calls connect_assets method on assets. Returns boolean if successful
        :param group_name: Maya node name of validation group
        :return:
        """

        selected_objects = pm.ls(sl=True)

        if selected_objects is None:
            return False

        is_success = ValidationGroups.connect_assets_to_validation_group(selected_objects, group_name)

        return is_success

    @staticmethod
    def disconnect_assets_from_validation_group(asset_list, group_name='anim_validator'):

        group_dict = ValidationGroups.__get_validation_group_dictionary()

        try:
            group_class = group_dict[group_name]
            meta_node = _get_pynode_by_class(group_class)

            for single_obj in asset_list:
                meta_node.disconnect_node(single_obj)

            return True

        except KeyError:
            print(f"Invalid validation group name: {group_name}")
            return False


class _AnimationValidator(DependentNode):
    """
    Animation Group Pynode

    Needs to run validation task:
    -Skeleton
    -Keyframe
    """

    dependent_node = ValidationGroups
    maya_node_name = 'animation_group'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace)
        return


class _PropValidator(DependentNode):
    """
    Prop Group Pynode

    Needs to run validation task:
    -Mesh
    -No Key
    -Material
    -Prefix
    """

    dependent_node = ValidationGroups
    maya_node_name = 'prop_group'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace)
        return


class _CharacterMeshValidator(DependentNode):
    """
    Character Mesh Group Pynode

    Needs to run validation task:
    -Rig (with paired CharacterSkelValidator)
    -Mesh
    -No Key
    """

    dependent_node = ValidationGroups
    maya_node_name = 'character_mesh_group'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace)
        return


class _CharacterSkelValidator(DependentNode):
    """
    Character Skel Group Pynode

    Needs to run validation task:
    -Rig (with paired CharacterMeshValidator)
    -Skeleton
    -No Key
    """
    dependent_node = ValidationGroups
    maya_node_name = 'character_skeleton_group'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace)
        return


_validation_groups_dict = {_AnimationValidator.maya_node_name: _AnimationValidator,
                  _PropValidator.maya_node_name: _PropValidator,
                  _CharacterMeshValidator.maya_node_name: _CharacterMeshValidator,
                  _CharacterSkelValidator.maya_node_name: _CharacterSkelValidator}


class ValidatorSettings(DependentNode):
    """
    Settings pynode for saving settings for Validation

    set_prop
    get_prop
    set_char
    get_char
    set_anim
    get_anim
    """

    dependent_node = Core
    maya_node_name = 'validation_settings'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace)
        return

    @classmethod
    def set_animation_group(cls, attributes_to_check, key_min, key_max):
        """
        :param attributes_to_check: list of string
        :param key_min: int
        :param key_max: int
        """

        if attributes_to_check:
            attributes_to_check = _convert_list_to_attribute_string(attributes_to_check)

        attributes_to_check = _check_and_convert_null_set_input(attributes_to_check, value_type='string')
        key_min = _check_and_convert_null_set_input(key_min, value_type='short')
        key_max = _check_and_convert_null_set_input(key_max, value_type='short')

        anim_node = _get_pynode_by_class(_AnimSettings)

        anim_node.set('attributes_to_check', attributes_to_check, 'string')
        anim_node.set('key_min', key_min, 'short')
        anim_node.set('key_max', key_max, 'short')

    @classmethod
    def get_animation_group(cls):
        """
        :return: [attributes_to_check] - list of string, [key_min] - int, [key_max] - int
        """

        anim_node = _get_pynode_by_class(_AnimSettings)

        attributes_to_check = anim_node.get('attributes_to_check', 'string')
        key_min = anim_node.get('key_min', 'short')
        key_max = anim_node.get('key_max', 'short')

        attributes_to_check = _check_and_convert_null_get_input(attributes_to_check)
        if attributes_to_check:
            attributes_to_check = _parse_attribute_string_to_list(attributes_to_check)

        key_min = _check_and_convert_null_get_input(key_min)
        key_max = _check_and_convert_null_get_input(key_max)

        return attributes_to_check, key_min, key_max

    @classmethod
    def set_character_group(cls, valid_materials_list, key_min, key_max):
        """
        :param valid_materials_list: list of string
        :param key_min: int
        :param key_max: int
        """

        if valid_materials_list:
            valid_materials_list = _convert_list_to_attribute_string(valid_materials_list)

        valid_materials_list = _check_and_convert_null_set_input(valid_materials_list, value_type='string')
        key_min = _check_and_convert_null_set_input(key_min, value_type='short')
        key_max = _check_and_convert_null_set_input(key_max, value_type='short')

        char_node = _get_pynode_by_class(_CharSettings)

        char_node.set('valid_materials_list', valid_materials_list, 'string')
        char_node.set('key_min', key_min, 'short')
        char_node.set('key_max', key_max, 'short')

    @classmethod
    def get_character_group(cls):
        """
        :return: [valid_materials_list] - list of string, [key_min] - int, [key_max] - int
        """

        char_node = _get_pynode_by_class(_CharSettings)

        valid_materials_list = char_node.get('valid_materials_list', 'string')
        key_min = char_node.get('key_min', 'short')
        key_max = char_node.get('key_max', 'short')

        valid_materials_list = _check_and_convert_null_get_input(valid_materials_list)
        if valid_materials_list:
            valid_materials_list = _parse_attribute_string_to_list(valid_materials_list)

        key_min = _check_and_convert_null_get_input(key_min)
        key_max = _check_and_convert_null_get_input(key_max)

        return valid_materials_list, key_min, key_max

    @classmethod
    def set_prop_group(cls, valid_materials_list, key_min, key_max, collision_prefix_list):
        """
        :param valid_materials_list: list of string
        :param key_min: int
        :param key_max: int
        :param collision_prefix_list: list of string
        """

        if valid_materials_list:
            valid_materials_list = _convert_list_to_attribute_string(valid_materials_list)

        if collision_prefix_list:
            collision_prefix_list = _convert_list_to_attribute_string(collision_prefix_list)

        valid_materials_list = _check_and_convert_null_set_input(valid_materials_list, value_type='string')
        key_min = _check_and_convert_null_set_input(key_min, value_type='short')
        key_max = _check_and_convert_null_set_input(key_max, value_type='short')
        collision_prefix_list = _check_and_convert_null_set_input(collision_prefix_list, value_type='string')

        prop_node = _get_pynode_by_class(_PropSettings)

        prop_node.set('valid_materials_list', valid_materials_list, 'string')
        prop_node.set('key_min', key_min, 'short')
        prop_node.set('key_max', key_max, 'short')
        prop_node.set('collision_prefix', collision_prefix_list, 'string')

    @classmethod
    def get_prop_group(cls):
        """
        :return: [valid_materials_list] - list of string, [key_min] - int, [key_max] - int, [collision_prefix] - string
        """

        prop_node = _get_pynode_by_class(_PropSettings)

        valid_materials_list = prop_node.get('valid_materials_list', 'string')
        key_min = prop_node.get('key_min', 'short')
        key_max = prop_node.get('key_max', 'short')
        collision_prefix = prop_node.get('collision_prefix', 'string')

        valid_materials_list = _check_and_convert_null_get_input(valid_materials_list)
        if valid_materials_list:
            valid_materials_list = _parse_attribute_string_to_list(valid_materials_list)

        collision_prefix = _check_and_convert_null_get_input(collision_prefix)
        if collision_prefix:
            collision_prefix = _parse_attribute_string_to_list(collision_prefix)

        key_min = _check_and_convert_null_get_input(key_min)
        key_max = _check_and_convert_null_get_input(key_max)

        return valid_materials_list, key_min, key_max, collision_prefix


class _AnimSettings(DependentNode):
    dependent_node = ValidatorSettings
    maya_node_name = 'anim_settings'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         attributes_to_check=('', 'string'),
                         key_min=(0, "short"),
                         key_max=(99, "short"))

        return


class _CharSettings(DependentNode):
    dependent_node = ValidatorSettings
    maya_node_name = 'char_settings'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         valid_materials_list=('', 'string'),
                         key_min=(0, "short"),
                         key_max=(99, "short"))

        return


class _PropSettings(DependentNode):
    dependent_node = ValidatorSettings
    maya_node_name = 'prop_settings'

    def __init__(self, parent=None, node_name=maya_node_name, node=None, namespace=""):
        super().__init__(parent, node_name, node, namespace,
                         valid_materials_list=('', 'string'),
                         key_min=(0, "short"),
                         key_max=(99, "short"),
                         collision_prefix=('', 'string'))

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
                         entry_keys=('', 'string'),
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
        OutputLog.set(output_node, 'entry_keys', '')
        OutputLog.set(output_node, 'target_object_name', '')

        return

    @classmethod
    def add_to_output_log(cls, log_entry, entry_key, target_object_name):
        output_maya_node = OutputLog.__get_output_maya_node()
        output_node = OutputLog(node=output_maya_node)

        cls.__append_to_output_node_attribute_strings(output_node, log_entry, attribute='output_log')
        cls.__append_to_output_node_attribute_strings(output_node, entry_key, attribute='entry_keys')
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

        :return: Returns 3 array as tuple

        [output_log]

        [entry_keys]

        [target_object_name]
        """
        output_maya_node = pm.ls('output_log')[0]
        output_node = OutputLog(node=output_maya_node)

        output_log = OutputLog.__get_output_node_attribute_value_as_list(output_node, attribute='output_log')

        entry_keys = OutputLog.__get_output_node_attribute_value_as_list(output_node, attribute='entry_keys')

        target_object_name = OutputLog.__get_output_node_attribute_value_as_list(output_node,
                                                                                 attribute='target_object_name')

        return output_log, entry_keys, target_object_name

    @staticmethod
    def __get_output_node_attribute_value_as_list(output_node, attribute='output_log'):
        long_string = OutputLog.get(output_node, attribute)
        value_as_list = OutputLog.__parse_string_to_list(long_string)

        return value_as_list
