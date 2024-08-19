# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.



"""
Qt Helper module for Maya and Metadata functionality, isolating dependency on pymel/metadata modules
"""

import pymel.core as pm
from validator_network_nodes import ValidationGroups


class QtMayaUtils:
    """
    Util class for pymel and maya related method calls
    """

    @staticmethod
    def get_maya_object_by_name(object_name):
        """
        Returns list of maya objects matching name using pymel .ls command
        """
        object_to_return = pm.ls(object_name)

        return object_to_return

    @staticmethod
    def select_object_by_name(maya_object_name):
        """
        Selects the given item in Maya using pymel .select command
        """
        if maya_object_name:
            pm.select(maya_object_name)

        return

    @staticmethod
    def deselect_object_by_name(maya_object_name):
        """
        Deselects the given item in Maya using pymel .select command
        """
        if maya_object_name:
            pm.select(maya_object_name, d=True)

        return

    @staticmethod
    def get_user_selected_maya_objects():
        """
        Returns user selected objects in maya using pymel .ls command
        """
        selected_objects = pm.ls(sl=True)
        return selected_objects

    @staticmethod
    def get_scene_materials():
        """
        Returns all materials that exist in maya scene using pymel .ls command
        """

        material_list = []
        # get all shading engines
        for shading_engine in pm.ls(type=pm.nt.ShadingEngine):
            # iterate through material connections
            for material in shading_engine.surfaceShader.listConnections():
                # return material as iterable
                material_list.append(str(material))

        # remove duplicates
        material_list = list(set(material_list))
        return material_list


class QtMetadataUtils:
    """
    Util class for metadata node calls
    """

    @staticmethod
    def get_validator_group_names():
        """
        Gets string list of validator group nodes from metadata module
        """
        names = ValidationGroups.get_name_of_all_group_maya_nodes()
        return names

    @staticmethod
    def get_validation_group_assets(group_name='anim_validation'):
        """
        Gets pymel maya objects from group name.
        Names should be validated from get_validator_group_names output.
        """
        assets = ValidationGroups.get_group_assets(group_name)
        return assets

    @staticmethod
    def connect_selected_maya_objects_to_validation_group(group_name='anim_validation'):
        """
        Attempts to connect user selected maya objects to validation group.
        :param group_name: Maya node name of validation group
        :return [is_success] - success boolean
        """
        is_success = ValidationGroups.connect_selected_maya_objects_to_validation_group(group_name)

        return is_success

    @staticmethod
    def connect_objects_to_validation_group(asset_list, group_name='anim_validation'):
        """
        Connects asset list from validation group.
        :param asset_list: Pymel asset list
        :param group_name: Maya node name of validation group
        :return [is_success] - success boolean
        """
        is_success = ValidationGroups.connect_assets_to_validation_group(asset_list, group_name)
        return is_success

    @staticmethod
    def disconnect_objects_from_validation_group(asset_list, group_name='anim_validation'):
        """
        Disconnects asset list from validation group.
        :param asset_list: Pymel asset list
        :param group_name: Maya node name of validation group
        :return [is_success] - success boolean
        """
        is_success = ValidationGroups.disconnect_assets_from_validation_group(asset_list, group_name)
        return is_success
