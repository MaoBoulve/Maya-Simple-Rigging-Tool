# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

"""
Command module for handling metadata data
"""

from rigging_tasks import WeightPainting, SkeletonRigging, RigControl
from rigging_network_nodes import WeightPaintingMetadataNode, RigControllersMetadataNode, SkeletonRigToolMetadataNode
import output_system_commands


class SkeletonRiggingCommands:

    @classmethod
    def set_rig_root_joint(cls, new_joint):
        """
        :param new_joint:
        :return:
        """

        is_valid = SkeletonRigging.check_is_object_a_valid_joint(new_joint)

        if is_valid:
            SkeletonRigToolMetadataNode.set_rig_root_joint(new_joint)

        return is_valid

    @classmethod
    def get_current_rig_root_joint(cls):
        joint = SkeletonRigToolMetadataNode.get_rig_root_joint()
        return joint

class RigControlCommands:

    @classmethod
    def set_target_control(cls, new_target_control):
        """

        :param new_target_control:
        :return:
        """

        is_valid = RigControl.check_is_object_a_valid_nurbs_shape(new_target_control)

        if is_valid:
            RigControllersMetadataNode.set_target_control_shape(new_target_control)

        return is_valid

    @classmethod
    def get_current_target_control(cls):

        control_shape = RigControllersMetadataNode.get_target_control_shape()
        return control_shape

    @classmethod
    def set_new_target_joint(cls, new_joint):
        """

        :param new_joint:
        :return:
        """

        is_valid = RigControl.check_is_object_a_valid_joint(new_joint)

        if is_valid:
            RigControllersMetadataNode.set_target_joint(new_joint)

        return is_valid

    @classmethod
    def get_current_target_joint(cls):

        target_joint = RigControllersMetadataNode.get_target_joint()
        return target_joint

class WeightPaintingCommands:

    @classmethod
    def set_weight_paint_joint(cls, new_joint):
        """
        :param new_joint: maya selected joint
        :return: is_success bool - set was success
        """

        is_valid = WeightPainting.check_is_object_a_valid_joint(new_joint)

        if is_valid:
            WeightPaintingMetadataNode.set_new_weight_paint_joint(new_joint)

        return is_valid

    @classmethod
    def set_mesh_to_paint(cls, new_mesh):
        """
        :param new_mesh: maya selected joint
        :return: is_success - set was success
        """
        is_valid = WeightPainting.check_is_object_a_valid_mesh(new_mesh)

        if is_valid:
            WeightPaintingMetadataNode.set_new_mesh(new_mesh)

        return is_valid

    @classmethod
    def set_vertex_list_to_paint(cls, vertex_list):
        """
        :param vertex_list: maya selected joint
        :return: is_success - set was success
        """
        is_valid = WeightPainting.check_is_object_valid_vertex_list(vertex_list)

        if is_valid:
            WeightPaintingMetadataNode.set_new_vertex_list(vertex_list)

        return is_valid

    @classmethod
    def apply_joint_weight_paint_on_metadata_mesh(cls, weight_paint_value):
        mesh = cls.get_current_weight_paint_mesh()
        joint = cls.get_current_weight_paint_joint()

        WeightPainting.set_mesh_weight_paint_influence_from_joint(skinned_mesh=mesh, joint_influence=weight_paint_value, joint=joint)
        return

    @classmethod
    def apply_joint_weight_paint_on_metadata_vertex(cls, weight_paint_value):
        vertex = cls.get_current_weight_paint_vertex_list()
        joint = cls.get_current_weight_paint_joint()

        WeightPainting.set_vertex_weight_paint_influence_from_joint(selected_vertex=vertex, joint_influence=weight_paint_value, joint=joint)
        return

    @classmethod
    def get_current_weight_paint_joint(cls):
        joint = WeightPaintingMetadataNode.get_weight_paint_joint()

        return joint


    @classmethod
    def get_current_weight_paint_mesh(cls):
        mesh = WeightPaintingMetadataNode.get_mesh()
        return mesh


    @classmethod
    def get_current_weight_paint_vertex_list(cls):
        return WeightPaintingMetadataNode.get_vertex_list()
