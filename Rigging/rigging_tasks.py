import pymel.core as pm


def test():
    create_control_shape_on_joint(pm.ls(sl=True)[0])


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
    # todo: create rig base??

def set_mesh_weight_paint_to_joint(skinned_mesh, joint):
    print("Flood weight paint")
    # todo: flood object influence with joint

def set_vertex_weight_paint_influence_for_joint(vertex, joint_influence, joint):
    print("Set vertex influence")
    # todo: set vertex influence from joint