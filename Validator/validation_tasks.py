# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Validation tasks module. Each exposed task has a .run() method with parameters defined in class definition. Results
of validation sent to output metadata and output to user in Qt Widget.

Public class TaskHub serves as public class for other modules to access validation tasks
"""

from abc import abstractmethod, ABC
import pymel.core as pm



class _ValidationTaskBase(ABC):
    """
    Base class for validation tasks. Task structure shared to allow for flexible parameter kwarg use and modular
    output as the project structure becomes more clear.

    For now, output is printed to editor log
    """

    __task_output_log = []
    _task_name = 'Base Validation'

    @classmethod
    def run(cls, objects_to_validate, **task_params):
        """
        Run method for validation task.
        Validates user parameters meet requirements for task, runs validation, outputs errors or success.

        :param objects_to_validate: list of maya objects, found through pymel
        :param task_params: validation task parameters, see Class Definition for optional & required params
        :return: Updates output log metadata on validation completion/halt
        """

        cls.__task_output_log.clear()

        # visual start marker
        cls.__append_validation_task_start()

        # parameter validation
        is_parameter_error = cls.__check_user_parameters_valid(objects_to_validate, task_params)

        if is_parameter_error:
            cls.__append_readability_spacer_to_output_log()
            cls.__send_task_output_log_to_output_metadata()
            return

        # optional parameters per task check
        updated_params = cls._populate_optional_parameters(**task_params)

        # main validation check
        is_validation_error = cls._run_validation(objects_to_validate, **updated_params)

        # visual error/success markers
        if is_validation_error:
            cls.__append_error_log()
        else:
            cls.__append_success_log()

        # sends output log to metadata system
        cls.__send_task_output_log_to_output_metadata()

        return

    @classmethod
    def __append_validation_task_start(cls):
        """
        Output method for displaying start of validation task for better readability
        """

        cls._append_to_task_output_log(f"========= Running {cls._task_name} =========", entry_key='task_start')
        cls.__append_readability_spacer_to_output_log()

        return

    @classmethod
    def __append_readability_spacer_to_output_log(cls):
        """
        Readability spacer to give text more room to breathe in output log
        """
        cls._append_to_task_output_log('', entry_key='spacer')
        cls._append_to_task_output_log('', entry_key='spacer')

        return

    @classmethod
    def _append_to_task_output_log(cls, task_entry, entry_key='default', target_object_name='None'):
        """
        Appends a formatted entry to the task_output_log for additional end user debug tracing
        :param task_entry: string entry
        :param entry_key: entry key string, keys of note are 'task_start', 'task_success', 'task_failure'
        :param target_object_name: maya object related to task, if left as 'None' no object will be selected
        :return:
        """

        output_entry = [task_entry, entry_key, target_object_name]

        cls.__task_output_log.append(output_entry)

        return

    @classmethod
    def __check_user_parameters_valid(cls, objects_to_validate, task_params):
        """
        Wrapped method of parameter validation check

        :return: [is_error] - error bool
        """
        is_object_error = cls._check_objects_to_validate_error(objects_to_validate)
        is_param_error = cls._check_required_parameters_error(**task_params)

        is_error = is_object_error or is_param_error
        return is_error

    @classmethod
    def _check_objects_to_validate_error(cls, objects_to_check):
        """
        Validate objects passed in to run process meet a minimum input length.

        :return: [is_error] - bool
        """

        if len(objects_to_check) == 0:

            cls._append_to_task_output_log("No objects were passed in for validation task.", entry_key='error')
            return True

        else:

            return False

    @classmethod
    def _check_required_parameters_error(cls, **params):
        """
        Check for specific params are filled with a certain criteria value.

        :return: [is_error] - bool
        """

        return False

    @classmethod
    def __send_task_output_log_to_output_metadata(cls):
        """
        Sends the current validation task output log to the metadata node for processing by front end
        """
        from validator_network_nodes import OutputLog

        for single_entry in cls.__task_output_log:
            OutputLog.add_to_output_log(single_entry[0], single_entry[1], single_entry[2])

        return

    @classmethod
    def _populate_optional_parameters(cls, **params):
        """
        Check each parameter used in validation task, if value is None then set default value.

        :return: [params] - updated parameter list as dictionary of {argname : argvalue}. If no optional parameters,
        returns input kwargs value
        """

        return params

    @classmethod
    @abstractmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Main validation method.

        Runs through validation tasks defined by each class, accumulating logs of checks completed.

        :param objects_to_validate: list of maya objects, found through pymel
        :param params: kwarg defined by each deriving class

        :return: [is_error] - bool, determines final append for task
        """

        if len(params.items()) < 10:
            param_error = True
        else:
            param_error = False

        if len(objects_to_validate < 10):
            object_error = True
        else:
            object_error = False

        # should do a bulk bool OR check here for all tasks

        is_error = param_error or object_error

        return is_error

    @classmethod
    def __append_error_log(cls):
        """
        Simple failure output
        """
        output_string = f"      --------------  {cls._task_name} Caught Error In Assets ---------------      "

        cls._append_to_task_output_log(output_string, entry_key='task_failure')
        cls.__append_readability_spacer_to_output_log()

        return

    @classmethod
    def __append_success_log(cls):
        """
        Simple success output
        """
        output_string = f"        ******  {cls._task_name} Successful  ******        "

        cls._append_to_task_output_log(output_string, entry_key='task_success')
        cls.__append_readability_spacer_to_output_log()

        return

    @staticmethod
    def _get_list_as_string(object_list):
        """
        List to string parser for readability. Separated by ', '
        :param object_list: any type of list
        :return: [single_string] - string
        """

        single_string = ', '.join(str(x) for x in object_list)
        return single_string


class DemoTask(_ValidationTaskBase):
    """
    DemoTask can be used as a template validation task defining common loops that may need flexibility outside
    a defined abstract method structure.

    In class definition, define parameters for run() as method is defined in base class with no need for override.
    Make use of IDE readability tools.

    [example_parameter] - define like this

    [second_parameter] - double enter for spacing
    """

    _task_name = 'Demo Validation'

    @classmethod
    def _populate_optional_parameters(cls, optional_param=None, **params):
        """
        Method defines optional parameters for task inside the function arguments with a default None value.
        If arg is None, fill the parameter with a default value, then append to the params dictionary

        :param optional_param: Rename and define var structure here
        :param params: Packed parameters kwarg argument
        :return: [params] - returned kwargs value
        """

        if optional_param is None:
            print("optional_param not filled \n")
            optional_param = "Default"
        else:
            print("optional_param filled!")

        params["optional_param"] = optional_param

        return params

    @classmethod
    def _check_required_parameters_error(cls, required_param=None, **params):
        """
        Method defines required parameters for difficult to assume parameters (materials with no material name, etc.)

        If arg in declaration remains None, append to error_log and return True to catch error

        :param required_param: Rename and define var structure here
        :param params: Packed parameters kwarg argument
        :return: [is_error] is error bool
        """

        is_error = False

        if required_param is None:
            cls._append_to_task_output_log("Missing 'required_param' parameter",
                                           entry_key='error')
            is_error = True

        return is_error

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Main validation task.

        Note to NOT define any keyword args of the prior optional/default parameters or double
        arg errors will occur.

        All parameters needed for task will have been packed into [params] and should be called by dictionary key.

        ie. Calling variable valid_materials_list by using params['valid_materials_list']

        :param objects_to_validate: pymel maya objects
        :param params: validation parameters packed into a dictionary
        :return: [is_error] - error bool
        """

        is_template_error = cls.__template_error_finding_task(objects_to_validate,
                                                              params['optional_param'],
                                                              params['required_param'])

        is_test_error = False

        is_error = is_template_error or is_test_error

        return is_error

    @classmethod
    def __template_error_finding_task(cls, objects_to_validate, optional_param, required_param):
        """
        Template for an error finding task.

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param optional_param: Rename and comment structure
        :param required_param: Rename and comment structure
        :return: [is_error] - error bool
        """
        is_error = False

        print(f"Objects are {objects_to_validate}, Optional is {optional_param}, Required is {required_param}")

        if optional_param == "Default":

            cls._append_to_task_output_log("Error! Optional param was left default",
                                           entry_key='error')

        return is_error


class SkelValidation(_ValidationTaskBase):
    """
    Validation class for iterating through a list of root joints for valid hierarchy.

    Run requirements:

    [objects_to_validate] - list of root joints
    """

    _task_name = 'Skeleton Validation'

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Skeleton validation task. Has single error finding task looking for invalid hierarchy objects

        :param objects_to_validate: pymel maya objects
        :return: [is_error] - error bool
        """

        invalid_objects_error = cls.__find_non_joints_in_hierarchy(objects_to_validate)

        is_error = invalid_objects_error

        return is_error

    @classmethod
    def __find_non_joints_in_hierarchy(cls, root_joints):
        """
        Error finding task looking for invalid hierarchy objects
        :param root_joints: skeleton group assets
        :return: [is_error] - error bool
        """

        is_error = False

        # ALL descendants of skeleton export should be joints
        object_children = pm.listRelatives(root_joints, allDescendents=True, parent=False, type='transform')
        hierarchy_joints = pm.ls(object_children, type='joint')

        # create list of only invalid objects
        invalid_objects = [obj for obj in object_children if obj not in hierarchy_joints]

        # removes invalid objects that are children to other invalid objects
        filtered_objects = cls.__filter_for_joint_parents(invalid_objects)

        # append to error log if error
        if filtered_objects:
            is_error = True

            for single_obj in filtered_objects:
                cls.__append_hierarchy_error(single_obj)

        return is_error

    @classmethod
    def __filter_for_joint_parents(cls, invalid_objects_list):
        """
        Filter method looking only for objects directly parented to joints
        :param invalid_objects_list: maya pymel objects
        :return: [invalid_objects_list] - list of string, updated list
        """

        for single_obj in invalid_objects_list:
            object_parent = pm.listRelatives(single_obj, parent=True)

            if pm.objectType(object_parent) != 'joint':
                invalid_objects_list.remove(single_obj)

        return invalid_objects_list

    @classmethod
    def __append_hierarchy_error(cls, invalid_object):
        """
        Format error method for invalid objects.
        :param invalid_object: pymel maya object
        """

        object_parent = pm.listRelatives(invalid_object, parent=True)
        response_string = f"Joint [{object_parent[0]}] has invalid child object: {invalid_object}"

        cls._append_to_task_output_log(response_string, entry_key='error', target_object_name=str(object_parent[0]))

        return


class MaterialValidation(_ValidationTaskBase):
    """
    Validation class for iterating through a list of meshes for use of a limited set of materials

    Run requirements:

    [objs_to_validate] - objects to check materials, validated if meshes

    [valid_materials] - material names, require at least 1 material name

    """

    _task_name = 'Material Validation'

    @classmethod
    def _check_objects_to_validate_error(cls, objects_to_check):
        """
        Checking if objects have shape objects and thus materials to check
        :param objects_to_check: pymel maya objects
        :return: [is_error] - error bool
        """
        input_length_error = super()._check_objects_to_validate_error(objects_to_check)

        material_error = False

        for single_obj in objects_to_check:
            if single_obj.getShape() is None:
                cls._append_to_task_output_log(f"Object without material in validation group: {single_obj}",
                                               entry_key="error", target_object_name=single_obj)
                material_error = True

        is_error = material_error or input_length_error

        return is_error

    @classmethod
    def _check_required_parameters_error(cls, valid_materials=None, **params):
        """
        Material validation requires at least 1 material passed in.
        :param valid_materials: list of string, Validation Required Parameter
        :return: [is_error] - error_bool
        """
        is_error = False

        if valid_materials is None:
            cls._append_to_task_output_log("Require at least 1 material in Valid Materials list", entry_key='error')

            is_error = True

        return is_error

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Task validation method checking objects for certain material names

        :param objects_to_validate: Objects to validate
        :param params: expecting param['valid_materials']
        :return: [is_error]: error bool
        """

        invalid_materials_error = cls.__find_invalid_materials_on_objects(objects_to_validate,
                                                                          params['valid_materials'])

        is_error = invalid_materials_error

        return is_error

    @classmethod
    def __find_invalid_materials_on_objects(cls, objects_to_check, valid_materials):
        """
        Gathers all materials in objects, filters out any matching valid materials list

        :param objects_to_check: maya pymel objs
        :param valid_materials: list of string
        :return: [is_error]: error bool
        """
        is_error = False

        # compares unique materials to valid materials list, prints any remaining list
        for single_obj in objects_to_check:
            materials_as_strings = cls.__get_unique_materials_from_object(single_obj)

            invalid_materials = [material for material in materials_as_strings if material not in valid_materials]

            if invalid_materials:
                is_error = True
                cls.__append_invalid_material_error(single_obj, invalid_materials)

        return is_error

    @classmethod
    def __get_unique_materials_from_object(cls, single_obj):
        """
        Gets materials from object via shader nodes
        :param single_obj: pymel maya object
        :return: [material_strings_list] - list of materials
        """

        # if single_obj.getShape():
        # previously had validation, but parameters validate

        shader_nodes = cls.__get_shader_nodes_from_transform_object(single_obj)
        found_materials = cls.__get_materials_from_shader_nodes(shader_nodes)

        material_strings_list = [str(x) for x in found_materials]
        material_strings_list = list(set(material_strings_list))
        # convert to set then back to list to clear duplicates

        return material_strings_list

    @classmethod
    def __get_shader_nodes_from_transform_object(cls, transform_object):
        """
        Gets unique shader nodes
        :param transform_object: assumes pymel object is transform node tied to shape node (or is shape node)
        :return: list of shader nodes
        """
        shader_nodes = set()  # work with hash set, looking only for unique shader node connections

        # get shape node -> shader node(s)
        shader_nodes.update(transform_object.getShape().listConnections(type='shadingEngine'))

        return shader_nodes

    @classmethod
    def __get_materials_from_shader_nodes(cls, shader_nodes_list):
        """
        Gets all materials connected to shader nodes
        :return [material_nodes] - list of materials
        """
        material_nodes = []
        for shader in shader_nodes_list:
            material_nodes = pm.ls(shader.listConnections(), materials=True)

        return material_nodes

    @classmethod
    def __append_invalid_material_error(cls, source_object, invalid_materials):
        """
        Formats error string
        """
        response_string = f"[{source_object}] has invalid material(s): {invalid_materials}"

        cls._append_to_task_output_log(response_string, entry_key='error', target_object_name=str(source_object))

        return


class KeyframeValidation(_ValidationTaskBase):
    """
    Validation class for checking objects have keyframes for all keys in range, for given attributes

    Run requirements:

    [objects_to_check] - pymel maya objects list

    [attribute_list] - string list, keyable attributes to check, OPTIONAL

    [min_key] - minimum integer keyframe, OPTIONAL

    [max_key] - max integer keyframe, OPTIONAL
    """

    _task_name = 'Keyframe Validation'

    @classmethod
    def _populate_optional_parameters(cls, attribute_list=None, min_key=None, max_key=None, **params):
        """
        :param attribute_list: string list of attributes, defaults to all 10 attributes
        :param min_key: minimum key, defaults to using the slider play min range
        :param max_key: maximum key, defaults to slider play max range

        :param params: Packed parameters kwarg argument
        :return: updated [params] list
        """

        if attribute_list is None:
            attribute_list = cls.__get_default_keyframe_attributes_to_check()

        tmp_min, tmp_max = cls.__get_current_playback_range()
        if min_key is None:
            min_key = tmp_min
        if max_key is None:
            max_key = tmp_max

        params["attribute_list"] = attribute_list
        params["min_key"] = min_key
        params["max_key"] = max_key

        return params

    @classmethod
    def __get_default_keyframe_attributes_to_check(cls):
        return ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY',
                'scaleZ', 'visibility']

    @classmethod
    def __get_current_playback_range(cls):
        min_time = pm.playbackOptions(query=True, min=True)
        max_time = pm.playbackOptions(query=True, max=True)
        return min_time, max_time

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Task validation method checking for attribute keys and floating point keys

        :param objects_to_validate: pymel maya objects
        :param params: All validation parameters packed into a dictionary
        :return: [is_error] - error bool
        """

        # get all downstream joints
        objects_to_validate = cls.__get_all_hierarchy_objects_for_validation(objects_to_validate)

        # find any missing keys
        missing_keys_error = cls.__find_missing_attribute_keys(objects_to_validate, params['attribute_list'],
                                                               params['min_key'], params['max_key'])

        # find decimal keys
        floating_point_keys_error = cls.__find_floating_point_keys(objects_to_validate, params['attribute_list'],
                                                                   params['min_key'], params['max_key'])

        is_error = missing_keys_error or floating_point_keys_error

        return is_error

    @staticmethod
    def __get_all_hierarchy_objects_for_validation(objects_to_validate):
        """
        Gets all unique downstream objects
        :return: [hierarchy_objects] - unique list of pymel objects
        """
        hierarchy_objects = pm.listRelatives(objects_to_validate, allDescendents=True, type='joint')
        hierarchy_objects.extend(objects_to_validate)
        hierarchy_objects = list(set(hierarchy_objects))

        return hierarchy_objects

    @classmethod
    def __find_missing_attribute_keys(cls, objects_to_validate, attribute_list, min_key, max_key):
        """
        Finds any missing attribute keys in keyframe range

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param attribute_list: list of string, attributes to check
        :param min_key: Min keyframe to check
        :param max_key: Max keyframe to check
        :return: [is_error] - error_bool
        """

        is_error = False

        keyframe_range = range(int(min_key), int(max_key + 1))  # keyframe list to compare against
        keyframe_range = list(keyframe_range)

        for single_obj in objects_to_validate:

            for attrib in attribute_list:
                # gets list of attribute keys, compares against list
                attribute_keys = cls.__get_obj_attribute_keys(single_obj, attrib, min_key, max_key)
                missing_keys = [key for key in keyframe_range if key not in attribute_keys]

                if missing_keys:
                    cls.__append_missing_keyframe_error(single_obj, attrib, missing_keys)
                    is_error = True

        return is_error

    @classmethod
    def __get_obj_attribute_keys(cls, object_to_get_keys, single_attribute, key_min, key_max):
        """
        Gets all keys for attribute within keyframe range
        :param object_to_get_keys: single object
        :param single_attribute: list attribute
        :param key_min: min key range
        :param key_max: max key range
        :return: [attribute_keys] - list of all attribute keys
        """

        attribute_keys = pm.keyframe(object_to_get_keys, query=True, attribute=single_attribute,
                                     time=(key_min, key_max))

        return attribute_keys

    @classmethod
    def __append_missing_keyframe_error(cls, single_object, single_attribute, difference_in_keys):
        """
        Error format
        """
        response_string = f"{single_object} missing [{single_attribute}] keys at : {difference_in_keys}"

        cls._append_to_task_output_log(response_string, entry_key='error', target_object_name=str(single_object))

        return

    @classmethod
    def __find_floating_point_keys(cls, objects_to_validate, attribute_list, min_key, max_key):
        """
        Finds any decimal attribute keys in keyframe range

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param attribute_list: list of string, attributes to check
        :param min_key: Min keyframe to check
        :param max_key: Max keyframe to check
        :return: [is_error] - error_bool
        """

        is_error = False

        for single_obj in objects_to_validate:

            for attrib in attribute_list:
                # checks keys in range for any decimal keys
                attribute_keys = cls.__get_obj_attribute_keys(single_obj, attrib, min_key, max_key)
                floating_point_keys = cls.__get_floating_point_keyframes(attribute_keys)

                if floating_point_keys:
                    cls.__append_floating_point_key_error(single_obj, attrib, floating_point_keys)

                    is_error = True

        return is_error

    @classmethod
    def __get_floating_point_keyframes(cls, attribute_keys):
        """
        Checks all keys for remainder after modulo % 1
        """

        attribute_keys = [x % 1 for x in attribute_keys]
        floating_point_indices = [i for i, x in enumerate(attribute_keys) if x != 0.0]
        floating_point_keys = [attribute_keys[i] for i in floating_point_indices]

        return floating_point_keys

    @classmethod
    def __append_floating_point_key_error(cls, invalid_object, attribute, floating_point_keys):
        """
        Error formatting
        """
        response_string = f"{invalid_object} has decimal [{attribute}] keyframes at : {floating_point_keys}"
        cls._append_to_task_output_log(response_string, entry_key='error', target_object_name=str(invalid_object))
        return


class RigValidation(_ValidationTaskBase):
    """
        Validation class for checking character skeleton and mesh are rigged together correctly and correct hierarchy

        Run requirements:

        [objects_to_validate] - pymel maya object list

        [rig_root_joint] - Single rig root joint pymel obj, will throw error if any other objects present
        """

    _task_name = 'Rig Validation'

    @classmethod
    def _check_required_parameters_error(cls, rig_root_joint=None, **params):
        """
        Validation task requires root joint to properly check

        :param rig_root_joint: Single root joint, assumes single skeleton is used as rig for validation
        :param params: Packed parameters kwarg argument
        :return: [is_error] - error_bool
        """
        is_error = False

        if rig_root_joint is None or len(rig_root_joint) < 1:
            cls._append_to_task_output_log("Missing root joint, check validation groups", entry_key='error')

            return True

        if len(rig_root_joint) > 1:
            cls._append_to_task_output_log("Multiple objects passed to root joint, should only be 1 root joint",
                                           entry_key='error')
            return True

        return is_error

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Validation task checking for invalid hierarchy objects & vertex skin weights

        :param objects_to_validate: pymel maya objects
        :param params: All validation parameters packed into a dictionary
        :return: [is_error] - error_bool
        """

        rig_joints = cls.__get_rig_joint_hierarchy(params['rig_root_joint'])

        # finds any joints with influence on rig not part of hierarchy
        joints_error = cls.__find_invalid_joints_in_skin_bind(objects_to_validate, rig_joints)

        # finds vertex with improper weight painting
        vertex_error = cls.__find_invalid_vertexes(objects_to_validate, rig_joints)

        is_error = joints_error or vertex_error

        return is_error

    @classmethod
    def __get_rig_joint_hierarchy(cls, root_joint):
        """
        Gets all joint in hierarchy, does not need to check for invalid objects since hierarchy task handles
        """

        valid_joints = pm.listRelatives(root_joint, type='joint', allDescendents=True)
        valid_joints.extend(root_joint)

        return valid_joints

    @classmethod
    def __find_invalid_joints_in_skin_bind(cls, objects_to_validate, valid_joints):
        """
        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param valid_joints: Valid joints for skin binding

        :return: [is_error] - error_bool
        """

        is_error = False

        for single_obj in objects_to_validate:

            shape_node = cls.__get_shape_node(single_obj)
            skin_nodes_list = cls.__get_skin_cluster_nodes(shape_node)

            invalid_joints_error = cls.__check_skin_nodes_for_invalid_joints(single_obj, skin_nodes_list, valid_joints)
            if invalid_joints_error:
                is_error = True

        return is_error

    @classmethod
    def __get_shape_node(cls, object_to_get):
        """
        Gets shape node depending on shape method
        :param object_to_get:
        :return:
        """
        if pm.objectType(object_to_get) == 'mesh':
            return object_to_get
        elif pm.objectType(object_to_get) == 'transform':
            return object_to_get.getShape()
        else:
            # edge case of catching a hierarchy object without shape past the initial param validation
            cls._append_to_task_output_log(f"Mesh object without shape: {object_to_get}", entry_key='error',
                                           target_object_name=str(object_to_get))
            return []

    @classmethod
    def __get_skin_cluster_nodes(cls, shape_object):
        """
        Gets skin cluster nodes
        """
        skin_cluster_node_list = shape_object.listConnections(type='skinCluster')
        return skin_cluster_node_list

    @classmethod
    def __check_skin_nodes_for_invalid_joints(cls, single_obj, skin_cluster_node_list, valid_joints):
        """
        Iterates through skin cluster nodes for invalid joint connections

        :param single_obj: pymel mesh to check
        :param skin_cluster_node_list: All skin cluster connections
        :param valid_joints: Pymel joint objects
        :return: [is_error] - error_bool
        """
        is_error = False

        for skin_node in skin_cluster_node_list:
            invalid_joints = cls.__get_invalid_joints_from_skin_node(skin_node, valid_joints)

            if invalid_joints:
                cls.__append_string_for_invalid_skin_bind_joints_response(invalid_joints, single_obj)
                is_error = True

        return is_error

    @classmethod
    def __get_invalid_joints_from_skin_node(cls, skin_cluster_node, valid_joints):
        """
        Compares unique joints in connections to valid joints
        """
        skin_cluster_joints = skin_cluster_node.listConnections(type='joint')
        skin_cluster_joints = list(set(skin_cluster_joints))

        invalid_joints = [joint for joint in skin_cluster_joints if joint not in valid_joints]

        return invalid_joints

    @classmethod
    def __append_string_for_invalid_skin_bind_joints_response(cls, invalid_joints, skin_bind_object):
        """
        Error format
        """
        invalid_joints_string = cls._get_list_as_string(invalid_joints)
        response_string = (f"{skin_bind_object} has joints attached to skin "
                           f"cluster not part of valid joints: {invalid_joints_string}")

        cls._append_to_task_output_log(response_string, entry_key='error', target_object_name=str(skin_bind_object))

        return

    @classmethod
    def __find_invalid_vertexes(cls, objects_to_validate, valid_joints):
        """
        Task for finding vertexes with invalid weight painting

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param valid_joints: Valid joints for skin binding

        :return: [is_error] - error_bool
        """
        is_error = False

        for single_obj in objects_to_validate:

            shape_node = cls.__get_shape_node(single_obj)
            skin_cluster_node_list = cls.__get_skin_cluster_nodes(shape_node)
            vertex_list = cls.__get_shape_vertex_list(single_obj)

            invalid_vertex_error = cls.__check_skin_nodes_for_invalid_vertex(single_obj, skin_cluster_node_list,
                                                                             valid_joints, vertex_list)
            if invalid_vertex_error:
                is_error = True

        return is_error

    @classmethod
    def __get_shape_vertex_list(cls, shape_object):
        """
        Gets vertexes
        """
        vertex_list = shape_object.vtx
        return vertex_list

    @classmethod
    def __check_skin_nodes_for_invalid_vertex(cls, single_obj, skin_node_list, valid_joints, vertex_list):
        """
        Calculates total weight paint per vertex from valid_joints list. If total less than 1.0, throw error

        :param single_obj: single shape object
        :param skin_node_list: list of nodes on object
        :param valid_joints: list of skeleton joints
        :param vertex_list: list of vertex
        :return: [is_error] - error bool
        """

        is_error = False

        for skin_node in skin_node_list:

            invalid_vertex_list = cls.__get_vertex_with_invalid_rig_influence(vertex_list, skin_node, valid_joints)

            if invalid_vertex_list:
                cls.__append_invalid_vertex_list_error(invalid_vertex_list, single_obj)
                is_error = True

        return is_error

    @classmethod
    def __get_vertex_with_invalid_rig_influence(cls, vertex_list, skin_cluster_node, valid_rig_joints):
        """
        Calculates vertex skin weight from valid joints

        """
        invalid_vertex_list = []

        for vertex in vertex_list:

            skin_bind_weight = cls.__get_vertex_skin_weight_from_joints(vertex, skin_cluster_node, valid_rig_joints)

            if skin_bind_weight != 1.0:
                invalid_vertex_list.append(vertex)

        return invalid_vertex_list

    @classmethod
    def __get_vertex_skin_weight_from_joints(cls, vertex, skin_cluster_node, joints_to_query):
        weight = 0.0
        for joint in joints_to_query:

            try:  # throws error if joint is not part of the rig hierarchy
                skin_percent = pm.skinPercent(skin_cluster_node, vertex, query=True, transform=joint)
                if skin_percent:
                    weight += skin_percent
            except RuntimeError:
                continue

        return weight

    @classmethod
    def __append_invalid_vertex_list_error(cls, invalid_vertex_list, skin_bind_object):
        # invalid_vertex_list_string = _get_object_list_as_string(invalid_vertex_list)
        # previously appended vertex list to response string but was often not useful output and very long

        response_string = f"{skin_bind_object} vertexes with skin weight below 1.0 from valid rig"
        cls._append_to_task_output_log(response_string, entry_key='error', target_object_name=str(skin_bind_object))

        return


class MeshHierarchyValidation(_ValidationTaskBase):
    """
        Validation task checking for mesh only objects in hierarchy

        Run requirements:

        [objects_to_validate] - pymel maya object list
        """

    _task_name = 'Mesh Hierarchy Validation'

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Validation task for finding non-shape hierarchy objects

        :param objects_to_validate: pymel maya objects
        :param params: All validation parameters packed into a dictionary
        :return: [is_error] - error_bool
        """

        hierarchy_error = cls.__find_invalid_hierarchy_objects(objects_to_validate)

        is_error = hierarchy_error

        return is_error

    @classmethod
    def __find_invalid_hierarchy_objects(cls, objects_to_validate):
        """
        Checks for invalid object types in mesh hierarchy

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task

        :return: [is_error] - error_bool
        """
        is_error = False

        for single_obj in objects_to_validate:

            try:
                single_obj.getShape()
                invalid_objects = cls.__check_invalid_objects_in_prop_hierarchy(single_obj)

                if invalid_objects:
                    cls.__append_invalid_hierarchy_object_error(single_obj, invalid_objects)
                    is_error = True

            except RuntimeError:
                cls._append_to_task_output_log(f"{single_obj} is not a valid object for Mesh Hierarchy Validation.",
                                               entry_key='error')

                is_error = True

        return is_error

    @classmethod
    def __check_invalid_objects_in_prop_hierarchy(cls, prop_object):
        """
        Checks hierarchy for only mesh-type objects, returning any remaining objects

        :param prop_object: pymel maya object
        :return: [invalid_objects] - list of pymel maya objects
        """

        object_relatives = pm.listRelatives(prop_object, allDescendents=True)

        valid_objects = []
        valid_object_types = ['mesh']

        for obj_type in valid_object_types:
            object_filter = pm.ls(object_relatives, type=obj_type)
            valid_objects.extend(object_filter)

        invalid_objects = [single_obj for single_obj in object_relatives if single_obj not in valid_objects]

        # remove transform nodes
        invalid_objects = [single_obj for single_obj in invalid_objects if pm.objectType(single_obj) != 'transform']

        return invalid_objects

    @classmethod
    def __append_invalid_hierarchy_object_error(cls, root_object, invalid_objects):
        """Error format"""
        objects_as_string = cls._get_list_as_string(invalid_objects)

        formatted_string = f"Prop root object [{root_object}] has invalid objects in hierarchy: {objects_as_string}"

        cls._append_to_task_output_log(formatted_string, entry_key='error', target_object_name=str(root_object))

        return


class MeshNodeConnectionValidation(_ValidationTaskBase):
    """
        Validation task searching for invalid node connections ['skinCluster', 'joint']

        Run requirements:

        [objects_to_validate] - pymel maya object list
        """

    _task_name = 'Node Connection Validation'

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        :param objects_to_validate: pymel maya objects
        :param params: All validation parameters packed into a dictionary
        :return: [is_error] - error_bool
        """

        node_error = cls.__find_invalid_node_connections(objects_to_validate)

        is_error = node_error

        return is_error

    @classmethod
    def __find_invalid_node_connections(cls, objects_to_validate):
        """
        Checks hierarchy node connections for invalid types

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :return: [is_error] - error_bool.
        """

        is_error = False

        for single_obj in objects_to_validate:
            invalid_tuple_error = cls.__check_for_invalid_node_connection(single_obj)

            if invalid_tuple_error:
                is_error = True

        return is_error

    @classmethod
    def __check_for_invalid_node_connection(cls, object_to_check):
        """
        Checks for invalid node types in hierarchy's connections

        :param object_to_check: root pymel object
        :return: [is_error] - error bool
        """

        # currently only looking for rig related node connections, should extend
        invalid_node_types = ['skinCluster', 'joint']
        is_error = False

        all_hierarchy_objects = [object_to_check]
        all_hierarchy_objects.extend(pm.listRelatives(object_to_check, allDescendents=True))

        for single_obj in all_hierarchy_objects:
            all_connection_nodes = list(set(pm.listConnections(single_obj)))

            invalid_nodes = []
            for node_type in invalid_node_types:
                filtered_nodes = pm.ls(all_connection_nodes, type=node_type)
                invalid_nodes.extend(filtered_nodes)

            if invalid_nodes:
                cls.__append_invalid_node_connection_error(single_obj, invalid_nodes)
                is_error = True

        return is_error

    @classmethod
    def __get_filtered_list_of_nodes(cls, object_to_retrieve_nodes):
        """
        Gets list of node connections to object, filtering 'poly' type nodes.

        :param object_to_retrieve_nodes: pymel object
        :return: [all_connections_nodes] - list of nodes
        """
        all_connection_nodes = list(set(pm.listConnections(object_to_retrieve_nodes)))
        all_connection_nodes = [obj for obj in all_connection_nodes if obj not in object_to_retrieve_nodes]

        nodes_to_clean = []
        for single_node in all_connection_nodes:
            if 'poly' in pm.objectType(single_node):
                nodes_to_clean.append(single_node)

        all_connection_nodes = [obj for obj in all_connection_nodes if obj not in nodes_to_clean]

        return all_connection_nodes

    @classmethod
    def __append_invalid_node_connection_error(cls, source_object, node_list):
        """Error format"""
        nodes_as_string = cls._get_list_as_string(node_list)
        formatted_string = f"{source_object} has invalid node connection(s): {nodes_as_string}"

        cls._append_to_task_output_log(formatted_string, entry_key='error', target_object_name=str(source_object))

        return


class EmptyKeysValidation(_ValidationTaskBase):
    """
        Validation task checking for ANY keys in key range

        Run requirements:

        [objects to validate] - pymel maya object list

        [min_key] - minimum key range to check

        [max_key] - maximum key range to check
        """

    _task_name = 'Empty Key Validation'

    @classmethod
    def _populate_optional_parameters(cls, min_key=None, max_key=None, **params):
        """
        :param min_key: minimum key, defaults to using the slider play min range
        :param max_key: maximum key, defaults to slider play max range

        :param params: Packed parameters kwarg argument
        :return: updated [params] list
        """

        tmp_min, tmp_max = cls.__get_current_playback_range()
        if min_key is None:
            min_key = tmp_min
        if max_key is None:
            max_key = tmp_max

        params["min_key"] = min_key
        params["max_key"] = max_key

        return params

    @classmethod
    def __get_current_playback_range(cls):
        """Gets current range as default value"""
        min_time = pm.playbackOptions(query=True, min=True)
        max_time = pm.playbackOptions(query=True, max=True)
        return min_time, max_time

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        :param objects_to_validate: pymel maya objects
        :param params: All validation parameters packed into a dictionary
        :return: [is_error] - error_bool
        """

        keyframe_error = cls.__find_any_attribute_keys(objects_to_validate, params['min_key'], params['max_key'])
        is_error = keyframe_error

        return is_error

    @classmethod
    def __find_any_attribute_keys(cls, objects_to_validate, min_key, max_key):
        """
        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param min_key: Minimum key range to check
        :param max_key: Maximum key range to check
        :return: [is_error] - error_bool
        """

        is_error = False

        hierarchy_objects = cls.__get_hierarchy_objects(objects_to_validate)

        for single_obj in hierarchy_objects:
            attribute_keys = cls.__get_all_attribute_keys_in_range(single_obj, min_key, max_key)

            if attribute_keys:
                attribute_keys = sorted(list(set(attribute_keys)))

                cls.__append_present_keyframes_error(single_obj, attribute_keys)

                is_error = True

        return is_error

    @classmethod
    def __get_hierarchy_objects(cls, objects_to_validate):
        """
        Gets all unique objects in hierarchy

        :param objects_to_validate:
        :return: list of pymel objects
        """
        hierarchy_objects = pm.listRelatives(objects_to_validate, allDescendents=True)
        hierarchy_objects.extend(objects_to_validate)
        hierarchy_objects = list(set(hierarchy_objects))
        return hierarchy_objects

    @classmethod
    def __get_all_attribute_keys_in_range(cls, object_to_check, key_min, key_max):
        """
        Gets all keys from query attribute in keyrange
        :param object_to_check: pymel object
        :param key_min: int keyframe
        :param key_max: int keyframe
        :return: list of float keys
        """
        attribute_keys = pm.keyframe(object_to_check, query=True, time=(key_min, key_max))
        return attribute_keys

    @classmethod
    def __append_present_keyframes_error(cls, source_object, attribute_keys):
        """Error output format """
        attribute_keys_list = cls._get_list_as_string(attribute_keys)

        keys_present_invalid_response = (f"Object [{source_object}] has keyframes at "
                                         f"following positions:[{attribute_keys_list}]")

        cls._append_to_task_output_log(keys_present_invalid_response, entry_key='error',
                                       target_object_name=str(source_object))

        return


class CollisionValidation(_ValidationTaskBase):
    """
    Validation class for checking collision for prop assets

    Run requirements:

    [objects to validate] - pymel maya object list

    [collision prefix] - list of collision prefix
    """

    _task_name = 'Collision Mesh Validation'


    @classmethod
    def _check_required_parameters_error(cls, collision_prefix=None, **params):
        """
        Method defines required parameters for difficult to assume parameters (materials with no material name, etc.)

        If arg in declaration remains None, append to error_log and return True to catch error

        :param collision_prefix: Collision prefix, ie UCX_, etc.
        :param params: Packed parameters kwarg argument
        :return: [is_error] is error bool
        """

        is_error = False

        if collision_prefix is None:
            cls._append_to_task_output_log("Missing 'collision_prefix' parameter",
                                           entry_key='error')
            is_error = True

        return is_error

    @classmethod
    def _run_validation(cls, objects_to_validate, **params):
        """
        Validation task for checking each mesh has a corresponding collision object

        :param objects_to_validate: pymel maya objects
        :param params: validation parameters packed into a dictionary
        :return: [is_error] - error bool
        """

        # get all downstream objects
        all_hierarchy_objects = cls.__get_hierarchy_mesh_objects(objects_to_validate)

        is_missing_collision_error = cls.__find_missing_collision_meshes(all_hierarchy_objects,
                                                                params['collision_prefix'])


        is_error = is_missing_collision_error

        return is_error

    @staticmethod
    def __get_hierarchy_mesh_objects(parent_objects):
        """
        Gets all unique downstream objects
        :return: [hierarchy_objects] - unique list of pymel objects
        """

        hierarchy_objects = pm.listRelatives(parent_objects, allDescendents=True, type='mesh')
        hierarchy_objects.extend(parent_objects)
        hierarchy_objects = list(set(hierarchy_objects))

        hierarchy_objects = pm.ls(hierarchy_objects, type='mesh')

        return hierarchy_objects

    @classmethod
    def __find_missing_collision_meshes(cls, objects_to_validate, collision_prefix_list):
        """
        Check hierarchy for collision mesh

        :param objects_to_validate: pymel maya objects, validated for basic criteria prior by validation task
        :param collision_prefix: Collision mesh prefix (ie UCX_)
        :return: [is_error] - error bool
        """
        is_error = False

        object_name_list = [str(single_obj) for single_obj in objects_to_validate]



        for single_obj in objects_to_validate:
            mesh_name = str(single_obj)

            "Assume error unless collision mesh is found."
            collision_mesh_found = False

            for single_prefix in collision_prefix_list:

                if single_prefix in mesh_name: # ignore any meshes with prefix already in name
                    collision_mesh_found = True
                else:
                    collision_mesh_name = single_prefix + mesh_name
                    "If prefix is UCX_ and mesh is 'sphere' looks for UCX_sphere"

                    if collision_mesh_name in object_name_list:
                        "If a collision mesh is found, mark error tentatively false"
                        collision_mesh_found = True


            if collision_mesh_found is False:
                cls.__append_missing_collision_error(single_obj, prefix_list=collision_prefix_list)
                is_error = True

        return is_error

    @classmethod
    def __append_missing_collision_error(cls, source_object, prefix_list):
        """Error output format """

        missing_collision_response = f"Object [{source_object}] missing collision mesh with prefix: {prefix_list}"

        cls._append_to_task_output_log(missing_collision_response, entry_key='error',
                                       target_object_name=str(source_object))

        return