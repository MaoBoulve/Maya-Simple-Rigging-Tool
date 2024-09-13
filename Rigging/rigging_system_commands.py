# Simple Rigging Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>..

"""
Command module for handling calls to metadata and rigging tasks. Handles cross module communication.
"""

from rigging_tasks import WeightPainting, SkeletonRigging, RigControl
from rigging_network_nodes import WeightPaintingMetadataNode, RigControllersMetadataNode, SkeletonRigToolMetadataNode
from output_system_commands import OutputLog


class SkeletonRiggingCommands:

    @classmethod
    def set_rig_root_joint(cls, new_joint):
        """
        Sets metadata rig root joint
        :param new_joint: maya object
        """

        is_valid = SkeletonRigging.check_is_object_a_valid_joint(new_joint)

        if is_valid:
            SkeletonRigToolMetadataNode.set_rig_root_joint(new_joint)
            OutputLog.add_to_output_log("-Set Root Joint success", "")

        return is_valid

    @classmethod
    def get_current_rig_root_joint(cls):
        """
        Gets metadata joint object
        :return: joint - maya object
        """
        joint = SkeletonRigToolMetadataNode.get_rig_root_joint()
        return joint

    @classmethod
    def load_rig_template(cls, template_name):
        """
        Creates joint chain from json file
        :param template_name: name of list in json file
        """
        SkeletonRigging.create_rig_base_from_json_file(joint_list_name=template_name, joint_notation="",
                                                       end_notation=True)
        return

    @classmethod
    def save_rig_template_from_metadata_joint_rig(cls, template_name):
        """
        Saves hierarchy of root rig to json file
        :param template_name: name of template
        """

        root_joint = cls.get_current_rig_root_joint()
        if root_joint:
            SkeletonRigging.save_rig_base_to_json_file(root_joint, joint_list_name=template_name)

        else:
            OutputLog.add_to_output_log("-Root joint does not exist", "")

        return

    @classmethod
    def mirror_rig_on_metadata_joint_rig(cls, search_text, replace_text, mirrorYZ=True, mirrorXY=True, mirrorZX=True):
        """
        Mirrors root rig joint hierarchy
        :param search_text: string, criteria substring to mirror joint
        :param replace_text: string, replaces search_text in mirrored joints
        :param mirrorYZ: bool, mirror across YZ plane
        :param mirrorXY: bool, mirror across XY plane
        :param mirrorZX: bool, mirror across ZX plane
        """

        root_joint = cls.get_current_rig_root_joint()

        if root_joint:
            SkeletonRigging.mirror_joint_chain(root_joint,
                                               mirrorYZ=mirrorYZ, mirrorXY=mirrorXY, mirrorXZ=mirrorZX,
                                               search_name=search_text, replace_name=replace_text)

        else:
            OutputLog.add_to_output_log("-Root joint does not exist", "")

        return

    @classmethod
    def delete_rig_template(cls, template_name):
        """
        Deletes a template from the json file
        :param template_name: string, name to delete
        """
        SkeletonRigging.delete_rig_template_from_json_file(template_to_remove=template_name)
        return

    @classmethod
    def get_rig_template_list(cls):
        """
        Gets all keys from rig template json file
        :return: rig_template_list - list of string
        """
        rig_template_list = SkeletonRigging.get_all_rig_template_names_from_json_file()
        return rig_template_list
class RigControlCommands:

    @classmethod
    def set_new_target_control(cls, new_target_control):
        """
        Sets metadata target control
        :param new_target_control: maya object
        """



        is_valid = RigControl.check_is_object_a_valid_nurbs_shape(new_target_control)

        if is_valid:
            RigControllersMetadataNode.set_target_control_shape(new_target_control)
            OutputLog.add_to_output_log("-Set Target Control success", "")

        return is_valid

    @classmethod
    def get_current_target_control(cls):
        """
        Gets metadata target control
        :return: control_shape - maya object
        """
        control_shape = RigControllersMetadataNode.get_target_control_shape()
        return control_shape

    @classmethod
    def set_new_target_joint(cls, new_joint):
        """
        Sets metadata target joint
        :param new_joint: maya object
        """

        is_valid = RigControl.check_is_object_a_valid_joint(new_joint)

        if is_valid:
            RigControllersMetadataNode.set_target_joint(new_joint)
            OutputLog.add_to_output_log("-Set Target Joint success", "")

        return is_valid

    @classmethod
    def get_current_target_joint(cls):
        """
        Gets current metadata target joint
        :return: target_joint - maya object
        """
        target_joint = RigControllersMetadataNode.get_target_joint()
        return target_joint

    @classmethod
    def create_control_on_target_joint(cls, joint_notation, control_notation, create_on_children):
        """
        Creates a control nurbs circle on metadata target joint, sets it as new target control
        :param joint_notation: string, substring to replace in joint
        :param control_notation: string, substring that overwrites the joint_notation
        :param create_on_children: bool, iterate through children of root joint
        """
        target_joint = cls.get_current_target_joint()

        if target_joint is None or target_joint == "":
            OutputLog.add_to_output_log("Target joint does not exist", "")
            return

        if create_on_children:
            root_control = RigControl.create_control_shape_on_all_joints(target_joint, joint_notation=joint_notation,
                                                                         controller_notation=control_notation)
            cls.set_new_target_control(root_control)
        else:

            target_control = RigControl.create_control_shape_on_joint(target_joint, joint_notation=joint_notation,
                                                                      controller_notation=control_notation)
            cls.set_new_target_control(target_control)

        OutputLog.add_to_output_log("-Create rig control object success", "")

        return

    @classmethod
    def parent_constraint_target_control_over_target_joint(cls, constrainTranslate, constrainRotate, constrainScale):
        """
        Parent constraint between control and joint
        :param constrainTranslate: bool
        :param constrainRotate: bool
        :param constrainScale: bool
        """
        target_control = cls.get_current_target_control()
        target_joint = cls.get_current_target_joint()

        if target_joint is None or target_control is None:
            OutputLog.add_to_output_log("-Target control or joint does not exist", "")
            return

        try:
            RigControl.parent_constrain_control_to_joint(control_shape=target_control, joint=target_joint,
                                                         constrainTranslate=constrainTranslate,
                                                         constrainRotate=constrainRotate,
                                                         constrainScale=constrainScale)
            OutputLog.add_to_output_log("-Parent constraint success", "")

        except RuntimeError as error:
            OutputLog.add_to_output_log(f"-Maya error: {error}", "")

        return

    @classmethod
    def point_constraint_target_control_over_target_joint(cls):
        """
        Point constraint between control and joint
        """
        target_control = cls.get_current_target_control()
        target_joint = cls.get_current_target_joint()

        if target_joint is None or target_control is None:
            OutputLog.add_to_output_log("-Target control or joint does not exist", "")
            return
        try:
            RigControl.point_constrain_control_to_joint(control_shape=target_control, joint=target_joint)
            OutputLog.add_to_output_log("-Point constraint success", "")

        except RuntimeError as error:
            OutputLog.add_to_output_log(f"-Maya error: {error}", "")

        return

    @classmethod
    def pole_vector_constraint_target_control_over_target_joint(cls):
        """
        Pole vector constraint
        """
        target_control = cls.get_current_target_control()
        target_joint = cls.get_current_target_joint()

        if target_joint is None or target_control is None:
            OutputLog.add_to_output_log("-Target control or joint does not exist", "")
            return

        try:
            RigControl.pole_vector_constrain_control_to_joint(control_shape=target_control, joint=target_joint)
            OutputLog.add_to_output_log("-Pole vector constraint success", "")

        except RuntimeError as error:
            OutputLog.add_to_output_log(f"-Maya error: {error}", "")

        return

    @classmethod
    def mirror_metadata_control_shapes(cls, search_text, replace_text, XYMirror, YZMirror, ZXMirror):
        """
        Mirror control shape hierarchy
        :param search_text: string, name criteria substring to mirror
        :param replace_text: string, replacement text
        :param XYMirror: bool, mirror across XY axis
        :param YZMirror: bool, mirror across YZ axis
        :param ZXMirror: bool, mirror across ZX axis
        """
        target_control = cls.get_current_target_control()

        if target_control is None:
            OutputLog.add_to_output_log("-Target control does not exist", "")
            return

        try:
            RigControl.mirror_control_shapes(root_control_shape=target_control, search_name=search_text,
                                             replace_name=replace_text, XYMirror=XYMirror, YZMirror=YZMirror, ZXMirror=ZXMirror)
            OutputLog.add_to_output_log("-Mirror controls success", "")

        except RuntimeError as error:
            OutputLog.add_to_output_log(f"-Maya error: {error}", "")

        return


class WeightPaintingCommands:

    @classmethod
    def set_weight_paint_joint(cls, new_joint):
        """
        Set metadata weight paint joint
        :param new_joint: maya selected joint
        :return: is_success bool - set was success
        """

        is_valid = WeightPainting.check_is_object_a_valid_joint(new_joint)

        if is_valid:
            WeightPaintingMetadataNode.set_new_weight_paint_joint(new_joint)
            OutputLog.add_to_output_log("-Set Joint success", "")

        return is_valid

    @classmethod
    def set_mesh_to_paint(cls, new_mesh):
        """
        Set metadata mesh
        :param new_mesh: maya selected joint
        :return: is_success - set was success
        """
        is_valid = WeightPainting.check_is_object_a_valid_mesh(new_mesh)

        if is_valid:
            WeightPaintingMetadataNode.set_new_mesh(new_mesh)
            OutputLog.add_to_output_log("-Set Mesh success", "")

        return is_valid

    @classmethod
    def set_vertex_list_to_paint(cls, vertex_list):
        """
        Set metadata vertex list
        :param vertex_list: maya selected joint
        :return: is_success - set was success
        """
        is_valid = WeightPainting.check_is_object_valid_vertex_list(vertex_list)

        if is_valid:
            WeightPaintingMetadataNode.set_new_vertex_list(vertex_list)
            OutputLog.add_to_output_log("-Set Vertex list success", "")

        return is_valid

    @classmethod
    def apply_joint_weight_paint_on_metadata_mesh(cls, weight_paint_value):
        """
        Apply flood weight paint on mesh
        :param weight_paint_value: float, weight paint value
        """
        mesh = cls.get_current_weight_paint_mesh()
        joint = cls.get_current_weight_paint_joint()

        if mesh is None or joint is None:
            OutputLog.add_to_output_log("-Mesh or Joint do not exist", "")
            return

        WeightPainting.set_mesh_weight_paint_influence_from_joint(skinned_mesh=mesh, joint_influence=weight_paint_value, joint=joint)

        OutputLog.add_to_output_log("-Mesh weight paint success", "")

        return

    @classmethod
    def apply_joint_weight_paint_on_metadata_vertex(cls, weight_paint_value):
        """
        Apply direct weight paint set value on vertex
        :param weight_paint_value: float, weight paint value
        """
        vertex = cls.get_current_weight_paint_vertex_list()
        joint = cls.get_current_weight_paint_joint()

        if vertex is None or joint is None:
            OutputLog.add_to_output_log("-Vertex or Joint do not exist", "")
            return

        WeightPainting.set_vertex_weight_paint_influence_from_joint(selected_vertex=vertex, joint_influence=weight_paint_value, joint=joint)

        OutputLog.add_to_output_log("-Vertex weight paint success", "")

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
