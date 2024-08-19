# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Module for calling validation tasks. Define the input requirements for validation task in each method for clarity
"""

import validation_tasks


"Task classes should only have 1 usage coming from the module methods"

def run_skeleton_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objects_to_validate] - list of root joints
    """
    validation_tasks.SkelValidation.run(objects_to_validate, **task_params)


def run_material_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objs_to_validate] - objects to check materials, validated if meshes

    [valid_materials] - material names, require at least 1 material name
    """
    validation_tasks.MaterialValidation.run(objects_to_validate, **task_params)


def run_keyframe_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objects_to_check] - pymel maya objects list

    [attribute_list] - string list, keyable attributes to check, OPTIONAL

    [min_key] - minimum integer keyframe, OPTIONAL

    [max_key] - max integer keyframe, OPTIONAL
    """
    validation_tasks.KeyframeValidation.run(objects_to_validate, **task_params)


def run_rig_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objects_to_validate] - pymel maya object list

    [rig_root_joint] - Single rig root joint pymel obj, will throw error if any other objects present
    """
    validation_tasks.RigValidation.run(objects_to_validate, **task_params)


def run_mesh_hierarchy_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objects_to_validate] - pymel maya object list
    """
    validation_tasks.MeshHierarchyValidation.run(objects_to_validate, **task_params)


def run_mesh_node_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objects_to_validate] - pymel maya object list
    """
    validation_tasks.MeshNodeConnectionValidation.run(objects_to_validate, **task_params)


def run_empty_key_validation(objects_to_validate, **task_params):
    """
    Run requirements:

    [objects to validate] - pymel maya object list

    [min_key] - minimum key range to check

    [max_key] - maximum key range to check
    """
    validation_tasks.EmptyKeysValidation.run(objects_to_validate, **task_params)


def run_collision_mesh_validation(objects_to_validate, **task_params):
    """
    Validation class for checking collision for prop assets

    Run requirements:

    [objects to validate] - pymel maya object list

    [collision_prefix] - collision prefix
    """
    validation_tasks.CollisionValidation.run(objects_to_validate, **task_params)