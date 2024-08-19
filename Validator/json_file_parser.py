# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Asset Validation Tool
# Asset Validation Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Asset Validation Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.


"""
Module for handling json file loading to automatically load json settings on startup
"""

import json

_module_file_path = __file__  # __file__ lists the full file path to the python file

class ValidatorJSONDataGetter:
    __json_filename = "validator_settings.json"

    """
    Class for reading validation settings from json class, converting inputs to format usable by metadata system
    
    Assumes JSON file is in the Validator folder & is named validator_settings.json. Need to match parameter order
    of each settings metadata node.
    """

    @classmethod
    def get_validator_json_data(cls):
        """
        Gets validation settings in format matching metadata list format, returning 3 lists

        [anim] - list: attributes_to_check, key_min, key_max

        [char] - list: valid_materials_list, key_min, key_max

        [prop] - list: valid_materials_list, key_min, key_max

        :return: anim, char, prop lists in order
        """

        json_data = _FileReader.get_json_data(cls.__json_filename)

        anim_settings_list = []
        char_settings_list = []
        prop_settings_list = []

        if json_data:
            anim_settings_list = list(json_data["anim_settings"].values())
            char_settings_list = list(json_data["char_settings"].values())
            prop_settings_list = list(json_data["prop_settings"].values())


        return anim_settings_list, char_settings_list, prop_settings_list



class _FileReader:
    """
    Class for reading local files. Assumes file is the same, or nested within, the same directory as the python file.
    """

    @classmethod
    def get_json_data(cls, json_filename):
        """
        Returns json data as dictionary.
        :param json_filename: string, local json name
        :return: [json_data] - single value
        """

        json_data = cls.__read_local_json_file(json_filename)

        if json_data is None:
            print(f"JSON not found: {json_filename}")

        return json_data

    # noinspection PyTypeChecker
    @classmethod
    def __read_local_json_file(cls, json_file_name):
        """
        Opens json file, searches for key in top level.
        :param json_file_name: string, json file name
        :return: [json_data] - json nested dictionary
        """

        json_file_path = _module_file_path.replace('json_file_parser.py', json_file_name)

        with open(json_file_path, 'r') as jsonfile:
            data = json.load(jsonfile)

        return data