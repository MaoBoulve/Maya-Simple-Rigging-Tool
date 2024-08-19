# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.


"""
Command module for overseeing the validation processes. User should be able to initialize validation system via
FrontEndCommands class methods.

Has high level access to validator_network_nodes and validation_tasks to collect assets, update settings, and
run validation tasks.

"""

from abc import abstractmethod, ABC
from validator_network_nodes import ValidatorSettings, OutputLog, ValidationGroups
import validation_control_hub as taskControl
from json_file_parser import ValidatorJSONDataGetter


class _ValidateCommandBase(ABC):
    """
    Validation command base class to provide structure to validation tasks

    Run calls 2 abstract methods for deriving classes to override:
    - _collect_group_assets
    - _run_validation_tasks
    """

    _asset_group_name = 'default_assets'

    @classmethod
    def run(cls, **kwargs):
        """
        Exposed run call for FrontEndCommands to call per each deriving class
        :param kwargs: dictionary of inputs
        """
        assets_to_run_task_on = cls._collect_group_assets()
        cls._run_validation_tasks(assets_to_run_task_on, **kwargs)

        return

    @classmethod
    def _collect_group_assets(cls):
        """
        Abstract method for collecting assets from metadata system for validation. Returns list of pymel objects
        """
        group_assets = ValidationGroups.get_group_assets(cls._asset_group_name)

        return group_assets

    @classmethod
    @abstractmethod
    def _run_validation_tasks(cls, group_assets, **kwargs):
        """
        Abstract method for validation tasks to run. Define keyword args with default None values per parameter of
        validation tasks

        :param group_assets: pymel maya object list
        :param kwargs: optional key word arguments
        """
        print("Getting abstract call")
        print(group_assets, kwargs)

        return


class _AnimationValidation(_ValidateCommandBase):
    """
    Validation command class for animation. Runs keyframe and skeletal hierarchy validation.
    kwargs to pass in:

    -attributes_to_check

    -key_min

    -key_max
    """

    _asset_group_name = 'animation_group'


    @classmethod
    def _run_validation_tasks(cls, group_assets, attributes_to_check=None, key_min=None, key_max=None, **kwargs):

        taskControl.run_keyframe_validation(group_assets, attribute_list=attributes_to_check, min_key=key_min,
                                            max_key=key_max)

        taskControl.run_skeleton_validation(group_assets)

        return


class _CharacterValidation(_ValidateCommandBase):
    """
    Validation command class for character. Runs material, rig, empty key, skeleton hierarchy, mesh hierarchy validation
    kwargs to pass in:

    -valid_materials_list

    -key_min

    -key_max
    """

    _asset_group_name = 'character_mesh_group'


    @classmethod
    def _run_validation_tasks(cls, group_assets, key_min=None, key_max=None, valid_materials_list=None, **kwargs):
        rig_joints = ValidationGroups.get_group_assets('character_skeleton_group')

        # rig + mesh tasks
        taskControl.run_material_validation(group_assets, valid_materials=valid_materials_list)
        taskControl.run_rig_validation(group_assets, rig_root_joint=rig_joints)
        taskControl.run_empty_key_validation(rig_joints, min_key=key_min, max_key=key_max)

        # skeleton tasks
        taskControl.run_skeleton_validation(rig_joints)
        taskControl.run_mesh_hierarchy_validation(group_assets)

        return

class _PropValidation(_ValidateCommandBase):
    """
    Validation command class for props. Runs material, mesh hierarchy, mesh node, empty key validation
    kwargs to pass in:

    -valid_materials_list

    -key_min

    -key_max

    -collision_prefix
    """

    _asset_group_name = 'prop_group'

    @classmethod
    def _run_validation_tasks(cls, group_assets, valid_materials_list=None, key_min=None, key_max=None,
                              collision_prefix=None, **kwargs):

        taskControl.run_material_validation(group_assets, valid_materials=valid_materials_list)
        taskControl.run_mesh_hierarchy_validation(group_assets)
        taskControl.run_mesh_node_validation(group_assets)
        taskControl.run_empty_key_validation(group_assets, min_key=key_min, max_key=key_max)
        taskControl.run_collision_mesh_validation(group_assets, collision_prefix=collision_prefix)

        return


class BackEndCommands:
    """
    Command class for handling initialization and data passing to and from back end metadata system
    """
    settings_node_initialized = False
    output_node_initialized = False

    @classmethod
    def update_settings(cls, anim_settings=None, character_settings=None, prop_settings=None):
        """
        Update settings expect list values passed in matching validation settings order

        :param anim_settings: attributes_to_check, key_min, key_max
        :param character_settings: valid_materials_list, key_min, key_max
        :param prop_settings: valid_materials_list, key_min, key_max, collision_prefix
        """

        if anim_settings:
            ValidatorSettings.set_animation_group(*anim_settings)
        if character_settings:
            ValidatorSettings.set_character_group(*character_settings)
        if prop_settings:
            ValidatorSettings.set_prop_group(*prop_settings)

        return

    @classmethod
    def run_validation(cls, animation_validation=False, character_validation=False, prop_validation=False):
        """
        Bulk call to run validation tasks. Gets current validation settings, clears output log metadata, and runs
        group tasks depending on keyword arg bools

        :param animation_validation: bool to run group validation
        :param character_validation: bool to run group validation
        :param prop_validation: bool to run group validation
        """
        anim, char, prop = BackEndCommands.get_settings()

        cls.clear_output_log()

        group_task_key = 'task_start'

        # class declaration of tasks defines **kwarg values to fill
        if animation_validation:
            OutputLog.add_to_output_log('ANIMATION GROUP', entry_key=group_task_key, target_object_name='')

            _AnimationValidation.run(attributes_to_check=anim[0], key_min=anim[1], key_max=anim[2])

        if character_validation:
            OutputLog.add_to_output_log('CHARACTER GROUP', entry_key=group_task_key, target_object_name='')

            _CharacterValidation.run(valid_materials_list=char[0], key_min=char[1], key_max=char[2])

        if prop_validation:
            OutputLog.add_to_output_log('PROP GROUP', entry_key=group_task_key, target_object_name='')

            _PropValidation.run(valid_materials_list=prop[0], key_min=prop[1], key_max=prop[2],
                                collision_prefix=prop[3])

        FrontEndCommands.open_outlog_widget()

        return

    @classmethod
    def get_settings(cls):
        """
        Gets current validator settings in tuple of order of validation task

        [anim] - tuple: attributes_to_check, key_min, key_max

        [char] - tuple: valid_materials_list, key_min, key_max

        [prop] - tuple: valid_materials_list, key_min, key_max

        :return: anim, char, prop tuples in order
        """

        anim = ValidatorSettings.get_animation_group()
        char = ValidatorSettings.get_character_group()
        prop = ValidatorSettings.get_prop_group()

        return anim, char, prop

    @classmethod
    def clear_output_log(cls):
        """
        Clears current output log
        """
        OutputLog.clear_output_log()

        return

    @classmethod
    def run_validation_from_json_file(cls):
        """
        Runs validation from json settings, running default settings if 'validator_settings.json'
        is not in Validator directory.
        """

        anim, char, prop = ValidatorJSONDataGetter.get_validator_json_data()

        cls.update_settings(anim_settings=anim, character_settings=char, prop_settings=prop)
        cls.run_validation(animation_validation=True, character_validation=True, prop_validation=True)

        return


class FrontEndCommands:
    """
    Command class for front end widget calls
    """
    qt_assets_widget = None
    qt_setting_widget = None
    qt_outlog_widget = None

    @classmethod
    def open_asset_tagging_widget(cls):
        """
        Instances asset tagging Qt widget and shows
        """
        import validator_asset_widget

        cls.qt_assets_widget = validator_asset_widget.AssetTaggingWidget()
        cls.qt_assets_widget.show()

        return

    @classmethod
    def open_validator_settings_widget(cls):
        """
        Instances validation settings Qt widget and shows
        """
        import validator_settings_widget

        cls.qt_setting_widget = validator_settings_widget.SettingsWidget()
        cls.qt_setting_widget.show()

        return

    @classmethod
    def open_outlog_widget(cls):
        """
        Instances output log Qt widget and shows
        :return:
        """
        import validator_output_widget

        cls.qt_outlog_widget = validator_output_widget.OutputWidget()
        cls.qt_outlog_widget.show()

        return

    @classmethod
    def rerun_validation_on_current_validator_widget_settings(cls):
        """
        Tells setting widget to rerun validation with current settings. If settings has not been initialized, opens
        widget.
        """

        if cls.qt_setting_widget is None:
            cls.open_validator_settings_widget()

        cls.qt_setting_widget.rerun_validation()

        return


def validate():
    """
    User facing command to run validation from maya python script
    """
    BackEndCommands.run_validation(animation_validation=True, character_validation=True, prop_validation=True)

    return


def run():
    """
    User facing command to open validation settings from maya python script
    """
    FrontEndCommands.open_validator_settings_widget()

    return


def assets():
    """
    User facing command to open validation settings from maya python script
    """
    FrontEndCommands.open_asset_tagging_widget()

    return

def validate_json():
    """
    User facing command to run validation using local json data
    """
    BackEndCommands.run_validation_from_json_file()

    return

def test_validation_task():
    """
    Debug method to test a single validation task by manually calling requisite steps

    1) Reset output log
    2) Gather assets
    3) Run validation task
    4) Open output widget
    """
    BackEndCommands.clear_output_log()

    group_assets = ValidationGroups.get_group_assets('prop_group')
    taskControl.run_collision_mesh_validation(group_assets, collision_prefix="_UCX")

    FrontEndCommands.open_outlog_widget()