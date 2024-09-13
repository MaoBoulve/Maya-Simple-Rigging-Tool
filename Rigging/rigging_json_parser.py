# Simple Rigging Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Module deriving from json file parser module to handle data tasks for rigging system
"""

from json_file_parser import FileWriter, FileReader


class RiggingJSONDataManagement:
    __json_filename = "rigging_joint_bases.json"

    """
    Class for reading validation settings from json class, converting inputs to format usable by metadata system

    Assumes JSON file is in the Validator folder & is named validator_settings.json. Need to match parameter order
    of each settings metadata node.
    """

    @classmethod
    def get_joint_list(cls, list_name_query="list_name"):
        """
        Gets joint list in json file
        :param list_name_query: string, name of list in json file
        """

        json_data = FileReader.get_json_data(cls.__json_filename)

        joint_list = []

        if json_data:
            joint_list = list(json_data[list_name_query])

        return joint_list

    @classmethod
    def add_joint_list_to_json_file(cls, joint_entry_list, list_name):
        """
        Adds a new entry to json file.
        :param joint_entry_list: List of entries in format [joint_name, [x,y,z] world position, parent_joint_name]
        :param list_name: Name of entry for getting list
        """

        FileWriter.write_json_value(entry_key=list_name, entry_value=joint_entry_list, json_filename=cls.__json_filename)

        return

    @classmethod
    def remove_joint_list_from_json_file(cls, list_to_remove):
        """
        Removes an entry from json file
        :param list_to_remove: string, list to remove
        """

        FileWriter.delete_json_value(entry_to_delete_key=list_to_remove, json_filename=cls.__json_filename)

        return

    @classmethod
    def get_all_joint_list_names(cls):
        """
        Gets list of all template joint lists in json file
        :return: template_list - list of string
        """
        template_list = []

        json_data = FileReader.get_json_data(cls.__json_filename)

        if json_data:
            template_list = list(json_data.keys())

        return template_list