# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Command module for user controlling simple rigging tool
"""

def open_simple_rig_tool():
    """
    Open simple rigging tool widget
    """

    import simple_rigging_tool_widget
    rig_widget = simple_rigging_tool_widget.SimpleRigToolWindowWidget()
    rig_widget.show()