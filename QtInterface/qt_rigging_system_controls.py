# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Command module for handling metadata data
"""

from rigging_tasks import WeightPainting
import pymel.core as pm

from rigging_network_nodes import OutputQueueLog, WeightPaintingMetadataNode


class Output:
    @classmethod
    def append_to_output_queue(cls, log_entry, log_target_object):
        OutputQueueLog.add_to_output_log(log_entry, log_target_object)
        return

    @classmethod
    def get_current_output_queue(cls):
        output = OutputQueueLog.get_output_log()

        return output

    @classmethod
    def clear_current_output_queue(cls):
        OutputQueueLog.clear_output_log()

        return

class WeightPaintingCommands:

    @classmethod
    def set_weight_paint_joint(cls, new_joint):
        """
        :param new_joint: maya selected joint
        :return: is_success bool - set was success
        """

        is_valid = WeightPainting.check_is_user_selected_a_valid_joint(new_joint)

        if is_valid:
            WeightPaintingMetadataNode.set_new_weight_paint_joint(new_joint[0])


        return is_valid

    @classmethod
    def set_mesh_to_paint(cls, new_mesh):
        """
        :param new_mesh: maya selected joint
        :return: is_success - set was success
        """
        is_valid = WeightPainting.check_is_user_selected_a_valid_mesh(new_mesh)

        if is_valid:
            WeightPaintingMetadataNode.set_new_mesh(new_mesh[0])

        return is_valid

    @classmethod
    def set_vertex_list_to_paint(cls, vertex_list):
        """
        :param vertex_list: maya selected joint
        :return: is_success - set was success
        """
        is_valid = WeightPainting.check_is_user_selected_valid_vertex_list(vertex_list)

        if is_valid:
            WeightPaintingMetadataNode.set_new_vertex_list(vertex_list)

        return is_valid

    @classmethod
    def apply_mesh_weight_paint(cls, weight_paint_value):
        mesh = pm.ls(WeightPaintingMetadataNode.get_mesh())[0]
        joint = pm.ls(WeightPaintingMetadataNode.get_weight_paint_joint())[0]

        WeightPainting.set_mesh_weight_paint_influence_from_joint(skinned_mesh=mesh, joint_influence=weight_paint_value, joint=joint)
        return

    @classmethod
    def apply_vertex_weight_paint(cls, weight_paint_value):
        vertex = pm.ls(WeightPaintingMetadataNode.get_vertex_list())
        joint = pm.ls(WeightPaintingMetadataNode.get_weight_paint_joint())[0]

        WeightPainting.set_vertex_weight_paint_influence_from_joint(selected_vertex=vertex, joint_influence=weight_paint_value, joint=joint)
        return

    @classmethod
    def get_current_weight_paint_joint(cls):
        joint = pm.ls(WeightPaintingMetadataNode.get_weight_paint_joint())
        if joint:
            return joint[0]
        return None

    @classmethod
    def get_current_weight_paint_mesh(cls):
        mesh = pm.ls(WeightPaintingMetadataNode.get_mesh())

        if mesh:
            return mesh[0]
        return None

    @classmethod
    def get_current_weight_paint_vertex_list(cls):
        return pm.ls(WeightPaintingMetadataNode.get_vertex_list())


    