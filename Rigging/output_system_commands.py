# Simple Rigging Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Module for handling access to Output metadata system
"""


from rigging_network_nodes import OutputLog


def append_to_output_log(log_entry, log_target_object=""):
    """
    Add a new entry to output log
    :param log_entry: string, entry
    :param log_target_object: maya object name, target of object (if applicable)
    """
    OutputLog.add_to_output_log(log_entry, log_target_object)
    return

def get_current_output_log():
    """
    Gets output log
    :return: output - list of string
    """
    output = OutputLog.get_output_log()

    return output

def clear_current_output_log():
    """
    Clears all entries from output log
    """
    OutputLog.clear_output_log()

    return