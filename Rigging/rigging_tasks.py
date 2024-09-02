# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

import pymel.core as pm
from rigging_system_commands import Output

# Edge cases handled by Maya:
#   - Meshes cannot have separate rigs with skin binds, get a 'mesh already has skinCluster' error


def create_control_shape_on_joint(joint):
    print("Create ctl")

    # parse joint name
    joint_name = str(joint)

    # get controller name from joint name, replacing _jnt with _ctl
    controller_name = joint_name.replace('_jnt', '')
    controller_name = controller_name + '_ctl'

    # orient controller to joint translation
    controller_center = [pm.getAttr(joint_name + '.translateX'),
           pm.getAttr(joint_name + '.translateY'),
           pm.getAttr(joint_name + '.translateZ')]
    controller_normal = [0, 0, 0]
    shape_radius = 3.0

    # create nurbs circle
    nurbs_circle = pm.circle(name=controller_name, radius=shape_radius,
                             center=controller_center, normal=controller_normal)

    # center pivot of created circle
    pm.xform(nurbs_circle, centerPivots=True)

    return nurbs_circle

def create_rig_base(rig_type):
    print("Create rig base")
    # todo: create rig base

def _append_to_user_output_log(new_entry):

    Output.append_to_output_queue(new_entry, "")
    return

class WeightPainting:

    @classmethod
    def set_mesh_weight_paint_influence_from_joint(cls, skinned_mesh, joint_influence, joint):
        """
        Sets skinned mesh to full rig influence to the single joint passed in

        :param skinned_mesh: Maya skinned mesh
        :param joint: Maya joint object
        :param joint_influence: 0-1 float value
        """
        print("Flood weight paint")

        shape_node = cls.__get_shape_node(skinned_mesh)
        skin_cluster = cls.__get_skin_cluster_nodes(shape_node)

        if len(skin_cluster) == 0:
            _append_to_user_output_log(f"-{skinned_mesh} is not a rigged mesh")
            return

        skin_cluster = skin_cluster[0]

        # doing a single skinPercent call is optimal and expected
        try:
            pm.skinPercent(skin_cluster, skinned_mesh.vtx, transformValue=(joint, joint_influence))
            _append_to_user_output_log(f"-Mesh weight paint for {skinned_mesh} successful")

        except RuntimeError as error_print:
            _append_to_user_output_log(f"-Error in attempting to apply weight paint: {error_print}")

        return

    @classmethod
    def __get_shape_node(cls, object_to_get):
        """
        Gets shape node depending on shape method
        :param object_to_get:
        """

        if pm.objectType(object_to_get) == 'mesh':
            return object_to_get
        elif pm.objectType(object_to_get) == 'transform':
            return object_to_get.getShape()
        else:
            # edge case of catching a hierarchy object without shape past the initial param validation
            return []

    @classmethod
    def __get_skin_cluster_nodes(cls, shape_object):
        """
        Gets skin cluster nodes

        :return: skin_cluster_node_list - list of skinCluster nodes with connection to rig
        """
        skin_cluster_node_list = shape_object.listConnections(type='skinCluster')
        return skin_cluster_node_list

    @classmethod
    def set_vertex_weight_paint_influence_from_joint(cls, selected_vertex, joint_influence, joint):
        """
        Sets the rig influence on the vertex(es) from the joint to a given value. Does a single skinPercent call for
        performance.

        :param selected_vertex: List of vertex maya objects
        :param joint_influence: Float value between 0-1
        :param joint: Joint object
        :return: is_success bool
        """
        print("Set vertex influence")

        # A selected vertex will have name format [shapeNode].vtx[i]

        vertex_list = [vertex for vertex in selected_vertex if '.vtx' in str(vertex)]

        if not vertex_list:
            _append_to_user_output_log("-No vertex were selected")
            return

        single_vertex = vertex_list[0]
        skinned_mesh_name = single_vertex.split('.vtx[')[0]
        skinned_mesh = pm.ls(skinned_mesh_name)[0]

        shape_node = cls.__get_shape_node(skinned_mesh)
        skin_cluster = cls.__get_skin_cluster_nodes(shape_node)

        if len(skin_cluster) == 0:
            _append_to_user_output_log(f"-{skinned_mesh} is not a rigged mesh")
            return

        skin_cluster = skin_cluster[0]

        # doing a single skinPercent call is optimal and expected
        try:
            pm.skinPercent(skin_cluster, vertex_list, transformValue=(joint, joint_influence))
            _append_to_user_output_log(f"-Vertex weight paint for {skinned_mesh} vertex successful")

        except RuntimeError as error_print:
            _append_to_user_output_log(f"-Error in attempting to apply weight paint: {error_print}")

        return True

    @classmethod
    def check_is_user_selected_a_valid_joint(cls, user_selected_object):

        if len(user_selected_object) != 1:
            # Multiple or zero objects selected
            return False

        if pm.objectType(user_selected_object) != 'joint':
            # Object is not a joint object
            return False

        return True

    @classmethod
    def check_is_user_selected_a_valid_mesh(cls, user_selected_object):

        if len(user_selected_object) != 1:
            # Multiple or zero objects selected
            return False

        if pm.objectType(user_selected_object) != 'mesh' and pm.objectType(user_selected_object) != 'transform':
            # Object is not a mesh/shape object
            return False

        return True

    @classmethod
    def check_is_user_selected_valid_vertex_list(cls, user_selected_list):

        if len(user_selected_list) == 0:
            # Zero objects selected
            return False

        invalid_list = [vertex for vertex in user_selected_list if '.vtx' not in str(vertex)]

        if invalid_list:
            # Non-vertex selected
            return False

        single_vertex = user_selected_list[0]
        skinned_mesh_name = single_vertex.split('.vtx[')[0]

        invalid_list = [vertex for vertex in user_selected_list if skinned_mesh_name not in str(vertex)]

        if invalid_list:
            # Vertex from multiple different shapes selected
            return False

        return True