# Asset Validation Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.

import pymel.core as pm
import output_system_commands

# Edge cases handled by Maya:
#   - Meshes cannot have separate rigs with skin binds, get a 'mesh already has skinCluster' error

def TDD_test_task():
    shape = pm.ls(sl=True)[0]

    RigControl.mirror_control_shapes(shape)

def create_rig_base(rig_type):
    print("Create rig base")
    # todo: create rig base

def _append_to_user_output_log(new_entry):

    output_system_commands.append_to_output_log(new_entry, "")

    return

class RigControl:
    """
    Rig setup class for creating nurbs shapes to control joints
    """

    @classmethod
    def create_control_shape_on_joint(cls, joint):

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

    @classmethod
    def set_control_shape_uniform_scale(cls, control_shape, new_scale):

        # parse control name
        control_shape_name = str(control_shape)
        control_scale = control_shape_name + '.scale'

        # set scale uniformly
        pm.setAttr(control_scale,new_scale, new_scale, new_scale)

        return

    @classmethod
    def set_control_shape_rotation(cls, control_shape, new_rotate_tuple=(0,0,0)):

        # parse control name
        control_shape_name = str(control_shape)
        control_rotate = control_shape_name + '.rotate'

        # set scale uniformly
        pm.setAttr(control_rotate, new_rotate_tuple)

    @classmethod
    def parent_constrain_control_to_joint(cls, control_shape, joint,
                                          translateX=True, translateY=True, translateZ=True,
                                          rotateX=True, rotateY=True, rotateZ=True,
                                          scaleX=True, scaleY=True, scaleZ=True,
                                          maintain_offset=True):
        skip_rotate, skip_scale, skip_translate = cls._make_vectors_for_axis_to_skip(rotateX, rotateY, rotateZ,
                                                                                     scaleX,scaleY,scaleZ,
                                                                                     translateX,translateY, translateZ)

        # Parent constraint ONLY constrains translate and rotate
        pm.parentConstraint(control_shape, joint, st=skip_translate, sr=skip_rotate, maintainOffset=maintain_offset)
        pm.scaleConstraint(control_shape, joint, sk=skip_scale, maintainOffset=maintain_offset)
        return

    @classmethod
    def _make_vectors_for_axis_to_skip(cls, rotateX, rotateY, rotateZ, scaleX, scaleY, scaleZ,
                                       translateX, translateY, translateZ):
        skip_translate = []
        skip_rotate = []
        skip_scale = []
        if not translateX:
            skip_translate.append("x")
        if not translateY:
            skip_translate.append("y")
        if not translateZ:
            skip_translate.append("z")
        if not rotateX:
            skip_rotate.append("x")
        if not rotateY:
            skip_rotate.append("y")
        if not rotateZ:
            skip_rotate.append("z")
        if not scaleX:
            skip_scale.append("x")
        if not scaleY:
            skip_scale.append("y")
        if not scaleZ:
            skip_scale.append("z")


        return skip_rotate, skip_scale, skip_translate

    @classmethod
    def point_constrain_control_to_joint(cls, control_shape, joint):
        pm.pointConstraint(control_shape, joint)

    @classmethod
    def pole_vector_constrain_control_to_joint(cls, control_shape, joint):
        pm.poleVectorConstraint(control_shape, joint)


    @classmethod
    def mirror_control_shapes(cls, root_control_shape, left_prefix='left_', right_prefix='right_', left_to_right=True,
                              xMirror=True, yMirror=False, zMirror=False):

        # Get all nurbs curves transforms from hierarchy

        hierarchy_nurbs = pm.listRelatives(root_control_shape, allDescendents=True, type='nurbsCurve')

        control_hierarchy = pm.listRelatives(hierarchy_nurbs, parent=True)
        control_hierarchy = pm.ls(control_hierarchy, type='transform')

        if left_to_right:
            search_prefix = left_prefix
            replace_prefix = right_prefix
        else:
            search_prefix = right_prefix
            replace_prefix = left_prefix

        control_to_mirror = [control for control in control_hierarchy if search_prefix in str(control)]
        control_parents = pm.listRelatives(control_to_mirror, parent=True, shapes=True)

        initial_control_group = pm.group(control_to_mirror, world=True)
        pm.xform(initial_control_group, pivots=[0,0,0], worldSpace=True)

        # create duplicate of the controls
        duplicate_controls_group = pm.duplicate(initial_control_group)

        # create scale vector
        x_scale, y_scale, z_scale = cls._make_axis_scale_values(xMirror, yMirror, zMirror)

        # mirror the new group
        mirror_group_scale = str(duplicate_controls_group[0]) + '.scale'
        pm.setAttr(mirror_group_scale, x_scale, y_scale, z_scale)

        hierarchy_nurbs = pm.listRelatives(duplicate_controls_group, allDescendents=True, type='nurbsCurve')
        mirrored_controls = pm.listRelatives(hierarchy_nurbs, parent=True)

        # renames mirrored group
        for single_control in mirrored_controls:
            old_name = str(single_control)
            new_name = old_name.replace(search_prefix, replace_prefix)
            pm.rename(single_control, new_name)

        control_parent_iterations = len(control_parents)

        for i in range(control_parent_iterations):
            parent_target = control_parents[i]

            # parent old control to prior parent
            pm.parent(control_to_mirror[i], parent_target)

            # check if parent should be to a new control
            if search_prefix in str(parent_target):
                parent_target = parent_target.replace(search_prefix, replace_prefix)

            # parent new control
            pm.parent(mirrored_controls[i], parent_target)

        return

    @classmethod
    def _make_axis_scale_values(cls, xMirror, yMirror, zMirror):
        if xMirror:
            x_scale = -1
        else:
            x_scale = 1
        if yMirror:
            y_scale = -1
        else:
            y_scale = 1
        if zMirror:
            z_scale = -1
        else:
            z_scale = 1
        return x_scale, y_scale, z_scale

    # TODO: mirror left to right/right to left and rename

class WeightPainting:
    """
    Rig setup class for weight painting a skinned mesh
    """
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
    def check_is_object_a_valid_joint(cls, user_selected_object):

        user_selected_object= pm.ls(sl=True)

        if len(user_selected_object) != 1:
            # Multiple or zero objects selected
            return False

        if pm.objectType(user_selected_object) != 'joint':
            # Object is not a joint object
            return False

        return True

    @classmethod
    def check_is_object_a_valid_mesh(cls, user_selected_object):

        if len(user_selected_object) != 1:
            # Multiple or zero objects selected
            return False

        if pm.objectType(user_selected_object) != 'mesh' and pm.objectType(user_selected_object) != 'transform':
            # Object is not a mesh/shape object
            return False

        return True

    @classmethod
    def check_is_object_valid_vertex_list(cls, user_selected_list):

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