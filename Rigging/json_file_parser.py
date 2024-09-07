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


class FileReader:
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


class FileWriter:
    """
    Class for writing to json files.
    """

    @classmethod
    def write_json_value(cls, entry_key, entry_value, json_filename):
        """
        Overwrites json file with new value.
        :param entry_key: string, dictionary key
        :param entry_value: string, new value for entry_key
        :param json_filename: string, local filename
        """

        json_file_path = _module_file_path.replace('json_file_parser.py', json_filename)

        with open(json_file_path, 'r') as json_file:
            # save data and set dict value to arg
            data = json.load(json_file)
            data[entry_key] = entry_value

        with open(json_file_path, 'w') as json_file:
            # write data, replacing whole data
            json_file.seek(0)
            json.dump(data, json_file, indent=4)

        return