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


class QtMayaUtils:
    """
    Util class for pymel and maya related method calls
    """

    @staticmethod
    def select_maya_object(maya_object):
        """
        Selects maya objects via standard pm.select() command
        :param maya_object: List of maya objs
        """

        pm.select(maya_object)
        return

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

    @staticmethod
    def count_distinct_vertex_from_sliced_list(vertex_list):
        full_vertex_list = []

        for list_entry in vertex_list:
            list_entry = str(list_entry)

            if ':' in list_entry:
                shape_name = list_entry.split('.vtx')[0]

                range_start, range_end = list_entry.split(':', 1)
                range_start = int(range_start.split('[')[1])
                range_end = int(range_end.split(']')[0]) + 1

                #pCubeShape1 + .vtx + [ + number + ]

                for vtx_num in range(range_start, range_end):
                    full_vertex_list.append(f"{shape_name}.vtx[{vtx_num}]")

            else:
                full_vertex_list.append(list_entry)

        return len(full_vertex_list)
