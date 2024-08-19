import pymel.core as pm


def test():
    print(pm.ls())


def create_control_shape_on_joint(joint):
    print("Create ctl")
    # todo: create controller from a selected joint - rename
    # todo: set controller to joint transform

def create_rig_base(rig_type):
    print("Create rig base")
    # todo: create rig base??

def set_mesh_weight_paint_to_joint(skinned_mesh, joint):
    print("Flood weight paint")
    # todo: flood object influence with joint

def set_vertex_weight_paint_influence_for_joint(vertex, joint_influence, joint):
    print("Set vertex influence")
    # todo: set vertex influence from joint