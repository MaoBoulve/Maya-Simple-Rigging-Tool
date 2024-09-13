# Simple Rigging Tool
# Copyright (C) 2024 Chris 'Nel' Mendoza

# This file is part of Simple Rigging Tool
# Simple Rigging Tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# Simple Rigging Tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with Foobar. If not, see <https://www.gnu.org/licenses/>.


import pymel.core as pm
import maya.mel as mel

import output_system_commands
import rigging_json_parser

# Edge cases handled by Maya:
#   - Meshes cannot have separate rigs with skin binds, get a 'mesh already has skinCluster' error

def TDD_test_task():
    print("TDD_test_task")
    # RigSetup.save_rig_base_to_json_file(pm.ls(sl=True)[0])

    return

def _append_to_user_output_log(new_entry):

    output_system_commands.append_to_output_log(new_entry, "")

    return


class SkeletonRigging:
    """
    Rig class for handling joint creation
    """

    @classmethod
    def create_rig_base_from_json_file(cls, joint_list_name="unreal", joint_notation="_jnt", end_notation=True):
        """
        Creates a joint chain based on saved json data.
        :param joint_list_name: string, Name of list to retrieve from json file
        :param joint_notation: string, string to append/prepend to joint for hierarchy clarity
        :param end_notation: bool, whether to append/prepend notation
        """

        try: # try-except catches when the json file was edited externally
            joint_list = rigging_json_parser.RiggingJSONDataManagement.get_joint_list(joint_list_name)

            cls._create_joint_chain_from_joint_entry_list(joint_list, joint_notation=joint_notation,
                                                          notation_at_end=end_notation)

            _append_to_user_output_log(f"-Created rig template: {joint_list_name}")


        except KeyError:
            _append_to_user_output_log(f"-Joint list not in JSON file: {joint_list_name}")


        return

    @classmethod
    def _create_joint_chain_from_joint_entry_list(cls, joint_entry_list, joint_notation, notation_at_end=True):
        """
        Creates a joint chain from a list of joint entries. If joints already exist, stops and deletes prior joints.
        :param joint_entry_list: list of entries with format [joint_name, [xyz position], joint_parent_name]
        :param joint_notation: string, notation
        :param notation_at_end: bool, notation is appended/prepended
        """

        # determine how notation should be handled
        if notation_at_end:
            joint_suffix = joint_notation
            joint_prefix = ''
        else:
            joint_suffix = ''
            joint_prefix = joint_notation

        joint_list = []
        parent_joint_name_list = []

        # iterate on joint entries list
        for joint_entry in joint_entry_list:

            pm.select(clear=True) # clears selection to avoid joint chain starting from a selected object

            joint_name = joint_prefix + joint_entry[0] + joint_suffix
            joint_position = joint_entry[1]

            if joint_entry[2] == 'NONE':
                parent_joint = None
            else:
                parent_joint = joint_prefix + joint_entry[2] + joint_suffix
            parent_joint_name_list.append(parent_joint)

            if pm.ls(joint_name):
                _append_to_user_output_log(f"-Object already exists: {joint_name}")
                pm.delete(joint_list)
                joint_list.clear()
                break

            new_joint = cls._create_joint(joint_name, joint_position)
            joint_list.append(new_joint)

        cls._iterate_parent_joint(joint_list, parent_joint_name_list)
        cls._orient_joint_list(joint_list)
        pm.select(clear=True)

        return

    @staticmethod
    def _create_joint(name='joint', position=(0,0,0)):
        """
        Creates and returns a joint with given parameters
        :param name: joint name
        :param position: x,y,z coordinate
        :return: joint - joint object
        """


        joint = pm.joint(position=position, name=name)

        return joint

    @staticmethod
    def _iterate_parent_joint(joint_list, parent_joint_name_list):
        """
        Parents joints in list to corresponding joint name
        :param joint_list: list of joints
        :param parent_joint_name_list: list of string, joint parent names
        :return:
        """

        iterations = len(joint_list)

        for i in range(iterations):
            if parent_joint_name_list[i]:
                pm.parent(joint_list[i], parent_joint_name_list[i])

        return


    @staticmethod
    def _orient_joint_list(joint_list):
        """
        Call mel command to orient all joints in list
        :param joint_list: list of maya joints
        """
        for joint in joint_list:
            # orient joints
            # edit flag not working in pymel so doing direct MEL command
            mel.eval(f'joint -e  -oj xyz -secondaryAxisOrient xup -ch -zso {str(joint)}')

        return

    @classmethod
    def mirror_joint_chain(cls, root_joint, mirrorYZ=True, mirrorXY=False, mirrorXZ=False,
                           search_name = 'left_', replace_name = 'right_'):
        """
        Mirrors all joints with certain string in their name across a specified axis
        :param root_joint: joint to search hierarchy for joints to mirror
        :param mirrorYZ: bool, mirror axis
        :param mirrorXY: bool, mirror axis
        :param mirrorXZ: bool, mirror axis
        :param search_name: string, joint string to search for
        :param replace_name: string, joint string to replace
        """

        pm.select(clear=True)
        joint_list = cls._get_joint_hierarchy(root_joint)
        print(joint_list)

        # looking for the first joints in side joint chains
        joints_to_mirror = [joint for joint in joint_list if search_name in str(joint)]
        joints_to_mirror = cls._search_for_first_joint_in_joints_to_mirror(joints_to_mirror, search_name)

        print(joints_to_mirror)

        for joint in joints_to_mirror:
            pm.mirrorJoint(joint, searchReplace=(search_name,replace_name), mirrorYZ=mirrorYZ,
                           mirrorXY=mirrorXY, mirrorXZ=mirrorXZ)


        pm.select(clear=True)

        _append_to_user_output_log(f"-Joint mirror successful")

        return

    @staticmethod
    def _get_joint_hierarchy(root_joint):
        """
        Gets all joints in hierarchy (including the root object passed in)
        :param root_joint: maya object, assumed joint but will not throw error for other types
        """

        joint_list = list()
        joint_list.append(root_joint)
        joint_list.append(pm.listRelatives(root_joint, allDescendents=True))
        joint_list = pm.ls(joint_list, type='joint')

        return joint_list

    @classmethod
    def _search_for_first_joint_in_joints_to_mirror(cls, joint_list, search_name):
        """
        Recursively searches for the first joint in a chain with the corresponding search_name
        :param joint_list: list of maya joints
        :param search_name: string, search criteria
        :return:
        """
        joints_to_remove = list()

        for joint in joint_list:
            parent = pm.listRelatives(joint, parent=True)[0]

            if search_name in str(parent):
                joints_to_remove.append(joint)

        joint_list = [joint for joint in joint_list if joint not in joints_to_remove]

        if joints_to_remove:
            joint_list = cls._search_for_first_joint_in_joints_to_mirror(joint_list, search_name)

        return joint_list

    @classmethod
    def save_rig_base_to_json_file(cls, root_joint, joint_list_name="new_base"):
        """
        Saves rig hierarchy to json file.
        :param root_joint: single maya object, assumed joint
        :param joint_list_name: string, name to append to json file
        """
        joint_list = cls._get_joint_hierarchy(root_joint)

        joint_entry_list = list()
        for joint in joint_list:
            joint_name = str(joint)

            joint_parent = pm.listRelatives(joint, parent=True)
            joint_parent = pm.ls(joint_parent, type='joint')

            if joint_parent:
                # gets world position by temporarily parenting to world
                joint_parent = str(joint_parent[0])
                pm.parent(joint, world=True)
                joint_position = list(pm.getAttr(joint_name + '.translate'))
                pm.parent(joint, joint_parent)
            else:
                joint_parent = 'NONE'
                joint_position = list(pm.getAttr(joint_name + '.translate'))

            joint_entry = [joint_name, joint_position, joint_parent]
            joint_entry_list.append(joint_entry)

        rigging_json_parser.RiggingJSONDataManagement.add_joint_list_to_json_file(joint_entry_list, joint_list_name)
        pm.select(clear=True)

        _append_to_user_output_log(f"-Saved new template: {joint_list_name}")

        return

    @classmethod
    def check_is_object_a_valid_joint(cls, object_to_check):

        if len(object_to_check) != 1:
            # Multiple or zero objects selected
            _append_to_user_output_log("-Single object not selected")
            return False

        if pm.objectType(object_to_check) != 'joint':
            # Object is not a joint object
            _append_to_user_output_log(f"-Object {object_to_check[0]} is not a Joint")

            return False

        return True

    @classmethod
    def delete_rig_template_from_json_file(cls, template_to_remove="rig_name"):
        locked_rigs = ['unity', 'unreal', 'simple']

        if template_to_remove in locked_rigs:
            _append_to_user_output_log(f"-Please delete default rig [{template_to_remove}] by directly editing 'rigging_joint_bases.json'")
            return


        try: # try-except catches when the json file was edited externally
            rigging_json_parser.RiggingJSONDataManagement.remove_joint_list_from_json_file(template_to_remove)

            _append_to_user_output_log(f"-Removed [{template_to_remove}] from templates")

        except KeyError:
            _append_to_user_output_log(f"-Joint list not in JSON file: {template_to_remove}")

        return

    @classmethod
    def get_all_rig_template_names_from_json_file(cls):

        rig_names = rigging_json_parser.RiggingJSONDataManagement.get_all_joint_list_names()

        rig_names = [name for name in rig_names if '_comment' not in name]

        return rig_names



class RigControl:
    """
    Rig setup class for creating nurbs shapes to control joints
    """

    @classmethod
    def create_control_shape_on_joint(cls, joint, joint_notation='_jnt', controller_notation='_ctl'):
        """
        Creates a controller based on the passed in joint
        :param joint: maya joint object
        :param joint_notation: string, notation to find
        :param controller_notation: string, notation to replace
        """
        # parse joint name
        joint_name = str(joint)

        # get controller name from joint name, replacing _jnt with _ctl
        controller_name = joint_name.replace(joint_notation, controller_notation)

        joint_parent = pm.listRelatives(joint, parent=True)

        if joint_parent:
            # gets world position by temporarily parenting to world
            joint_parent = str(joint_parent[0])
            pm.parent(joint, world=True)
            controller_center = list(pm.getAttr(joint_name + '.translate'))
            pm.parent(joint, joint_parent)

        else:
            controller_center = list(pm.getAttr(joint_name + '.translate'))


        # orient controller to joint translation
        shape_radius = 4.0

        # create nurbs circle
        nurbs_circle = pm.circle(name=controller_name, radius=shape_radius,
                                 center=controller_center)

        # center pivot of created circle
        pm.xform(nurbs_circle, centerPivots=True)

        if len(nurbs_circle) > 1:
            # nurbs command generates a second MakeNurbs object, slice list
            nurbs_circle = nurbs_circle[:1]

        return nurbs_circle

    @classmethod
    def create_control_shape_on_all_joints(cls, root_joint, joint_notation='_jnt', controller_notation='_ctl'):

        all_joints = cls._get_joint_hierarchy(root_joint)
        shape_to_return = None


        for joint in all_joints:
            created_shape = cls.create_control_shape_on_joint(joint=joint, joint_notation=joint_notation,
                                                              controller_notation=controller_notation)

            if joint == root_joint:
                shape_to_return = created_shape

        return shape_to_return

    @staticmethod
    def _get_joint_hierarchy(root_joint):
        """
        Gets all joints in hierarchy (including the root object passed in)
        :param root_joint: maya object, assumed joint but will not throw error for other types
        """

        joint_list = list()
        joint_list.append(root_joint)
        joint_list.append(pm.listRelatives(root_joint, allDescendents=True))
        joint_list = pm.ls(joint_list, type='joint')

        return joint_list

    @classmethod
    def parent_constrain_control_to_joint(cls, control_shape, joint,
                                          constrainTranslate=True,
                                          constrainRotate=True,
                                          constrainScale=True,
                                          maintain_offset=True):
        """
        Apply parent constraint with bools for the 10 settings applicable
        :param control_shape: shape object
        :param joint: joint object
        :param constrainTranslate: bool, constrain translate axis
        :param constrainRotate: bool, constrain translate axis
        :param constrainScale: bool, constrain translate axis
        :param maintain_offset: bool, move parented object or keep in place. False snaps child object to parent
        """


        skip_rotate, skip_scale, skip_translate = cls._make_vectors_for_axis_to_skip(constrainTranslate,
                                                                                     constrainRotate,
                                                                                     constrainScale)

        # Parent constraint ONLY constrains translate and rotate
        pm.parentConstraint(control_shape, joint, st=skip_translate, sr=skip_rotate, maintainOffset=maintain_offset)
        pm.scaleConstraint(control_shape, joint, sk=skip_scale, maintainOffset=maintain_offset)
        return

    @classmethod
    def _make_vectors_for_axis_to_skip(cls, constrainTranslate, constrainRotate, constrainScale):
        """
        Creates vectors for parent and scale constraint axis to skip. Parameters are all bool for axis to skip
        :return: skip_rotate, skip_scale, skip_translate
        """
        skip_translate = []
        skip_rotate = []
        skip_scale = []
        if not constrainTranslate:
            skip_translate.append(['x','y','z'])
        if not constrainRotate:
            skip_rotate.append(['x','y','z'])
        if not constrainScale:
            skip_scale.append(['x','y','z'])


        return skip_rotate, skip_scale, skip_translate

    @classmethod
    def point_constrain_control_to_joint(cls, control_shape, joint):
        """
        Simple point constraint from shape to joint
        :param control_shape: shape object
        :param joint: joint object
        """
        pm.pointConstraint(control_shape, joint)
        return

    @classmethod
    def pole_vector_constrain_control_to_joint(cls, control_shape, joint):
        """
        Simple vector constraint from shape to joint
        :param control_shape: shape object
        :param joint: joint object
        """

        pm.poleVectorConstraint(control_shape, joint)
        return

    @classmethod
    def mirror_control_shapes(cls, root_control_shape, search_name='left_', replace_name='right_',
                              XYMirror=True, YZMirror=False, ZXMirror=False):
        """
        Mirrors control objects across specified axis. Replaces search_name substring with replace_name substring
        :param root_control_shape: root shape maya object
        :param search_name: substring to determine shape should be mirrored
        :param replace_name: substring to put on mirrored objects
        :param XYMirror: bool, mirror across XY
        :param YZMirror: bool, mirror across YZ
        :param ZXMirror: bool, mirror across ZX
        """
        # Get all nurbs curves transforms from hierarchy

        control_to_mirror = cls._get_controls_to_mirror_from_hierarchy(root_control_shape, search_name)
        control_parents = pm.listRelatives(control_to_mirror, parent=True, shapes=True)

        duplicate_controls_group, initial_control_group = cls._group_and_duplicate_controls(control_to_mirror)

        # create scale vector
        x_scale, y_scale, z_scale = cls._make_axis_scale_values(XYMirror, YZMirror, ZXMirror)

        # mirror the new group
        cls._set_duplicate_group_scale_to_mirror(duplicate_controls_group, x_scale, y_scale, z_scale)

        # get control objects only
        hierarchy_nurbs = pm.listRelatives(duplicate_controls_group, allDescendents=True, type='nurbsCurve')
        mirrored_controls = pm.listRelatives(hierarchy_nurbs, parent=True)

        # renames mirrored group
        cls._rename_mirrored_controls(mirrored_controls, replace_name, search_name)

        cls._parent_mirrored_control_hierarchy(control_parents, control_to_mirror, mirrored_controls, replace_name,
                                               search_name)

        # delete group maya nodes
        pm.delete(initial_control_group)
        pm.delete(duplicate_controls_group)

        return

    @classmethod
    def _set_duplicate_group_scale_to_mirror(cls, duplicate_controls_group, x_scale, y_scale, z_scale):

        mirror_group_scale = str(duplicate_controls_group[0]) + '.scale'
        pm.setAttr(mirror_group_scale, x_scale, y_scale, z_scale)

        return

    @classmethod
    def _get_controls_to_mirror_from_hierarchy(cls, root_control_shape, search_name):
        hierarchy_nurbs = pm.listRelatives(root_control_shape, allDescendents=True, type='nurbsCurve')

        control_hierarchy = pm.listRelatives(hierarchy_nurbs, parent=True)
        control_hierarchy = pm.ls(control_hierarchy, type='transform')

        control_to_mirror = [control for control in control_hierarchy if search_name in str(control)]

        return control_to_mirror

    @classmethod
    def _group_and_duplicate_controls(cls, control_to_mirror):
        initial_control_group = pm.group(control_to_mirror, world=True)
        pm.xform(initial_control_group, pivots=[0, 0, 0], worldSpace=True)

        # create duplicate of the controls
        duplicate_controls_group = pm.duplicate(initial_control_group)

        return duplicate_controls_group, initial_control_group

    @classmethod
    def _make_axis_scale_values(cls, XYMirror, YZMirror, ZXMirror):
        """
        Makes axis scale values for mirroring control shapes.
        :param XYMirror: bool
        :param YZMirror: bool
        :param ZXMirror: bool
        :return: x_scale - int, y_scale - int, z_scale - int
        """
        if XYMirror:
            x_scale = 1
            y_scale = 1
            z_scale = -1

        elif YZMirror:
            x_scale = -1
            y_scale = 1
            z_scale = 1

        elif ZXMirror:
            x_scale = 1
            y_scale = -1
            z_scale = 1

        else:
            x_scale = 1
            y_scale = 1
            z_scale = 1

        return x_scale, y_scale, z_scale

    @classmethod
    def _rename_mirrored_controls(cls, mirrored_controls, replace_name, search_name):
        for single_control in mirrored_controls:
            old_name = str(single_control)
            new_name = old_name.replace(search_name, replace_name)
            pm.rename(single_control, new_name)

        return

    @classmethod
    def _parent_mirrored_control_hierarchy(cls, control_parents, control_to_mirror, mirrored_controls, replace_name,
                                           search_name):

        control_parent_iterations = len(control_parents)

        for i in range(control_parent_iterations):
            parent_target = control_parents[i]

            if parent_target is None or parent_target == "NONE":
                parent_to_world = True
            else:
                parent_to_world = False

            # parent old control to prior parent
            pm.parent(control_to_mirror[i], parent_target, world=parent_to_world)

            # check if parent should be to a new control
            if search_name in str(parent_target):
                parent_target = parent_target.replace(search_name, replace_name)

            # parent new control
            pm.parent(mirrored_controls[i], parent_target, world=parent_to_world)

        return



    @classmethod
    def check_is_object_a_valid_joint(cls, object_to_check):

        if len(object_to_check) != 1:
            # Multiple or zero objects selected
            _append_to_user_output_log("-Single object not selected")
            return False

        if pm.objectType(object_to_check) != 'joint':
            # Object is not a joint object
            _append_to_user_output_log(f"-Object {object_to_check[0]} is not a Joint")
            return False

        return True

    @classmethod
    def check_is_object_a_valid_nurbs_shape(cls, object_to_check):

        if len(object_to_check) != 1:
            # Multiple or zero objects selected
            _append_to_user_output_log("-Single object not selected")
            return False
        object_to_check = object_to_check[0]

        if pm.objectType(object_to_check) == 'transform':
            object_to_check = object_to_check.getShape()

        if pm.objectType(object_to_check) != 'nurbsCurve':
            # Object is not a nurbs object
            _append_to_user_output_log(f"-Object {object_to_check} is not a NURBS shape")
            return False

        return True


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
    def check_is_object_a_valid_joint(cls, object_to_check):

        if len(object_to_check) != 1:
            # Multiple or zero objects selected
            _append_to_user_output_log("-Single object not selected")
            return False

        if pm.objectType(object_to_check) != 'joint':
            # Object is not a joint object
            _append_to_user_output_log(f"-Object {object_to_check[0]} is not a joint")
            return False

        return True

    @classmethod
    def check_is_object_a_valid_mesh(cls, object_to_check):

        if len(object_to_check) != 1:
            # Multiple or zero objects selected
            _append_to_user_output_log("-Single object not selected")
            return False

        if pm.objectType(object_to_check) != 'mesh' and pm.objectType(object_to_check) != 'transform':
            # Object is not a mesh/shape object
            _append_to_user_output_log(f"-Object {object_to_check[0]} is not a mesh (or transform of a mesh object)")
            return False

        return True

    @classmethod
    def check_is_object_valid_vertex_list(cls, user_selected_list):

        if len(user_selected_list) == 0:
            _append_to_user_output_log("-No objects were selected")
            # Zero objects selected
            return False

        invalid_list = [vertex for vertex in user_selected_list if '.vtx' not in str(vertex)]

        if invalid_list:
            # Non-vertex selected
            _append_to_user_output_log("-Object(s) are not vertex")
            return False

        single_vertex = user_selected_list[0]
        skinned_mesh_name = single_vertex.split('.vtx[')[0]

        invalid_list = [vertex for vertex in user_selected_list if skinned_mesh_name not in str(vertex)]

        if invalid_list:
            # Vertex from multiple different shapes selected
            _append_to_user_output_log("-Vertex from different shapes selected")
            return False

        return True