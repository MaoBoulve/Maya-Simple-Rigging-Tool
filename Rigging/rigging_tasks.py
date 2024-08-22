import pymel.core as pm


def test():
    #create_control_shape_on_joint(pm.ls(sl=True)[0])

    # set_mesh_weight_paint_to_joint(pm.ls(sl=True)[0], pm.ls('test_flood')[0])
    set_selected_vertex_weight_paint_influence_for_joint(pm.ls(sl=True), 0.5, pm.ls('test_flood')[0])


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

    shape_node = __get_shape_node(skinned_mesh)
    skin_cluster = __get_skin_cluster_nodes(shape_node)
    skin_cluster = skin_cluster[0]

    # doing a single skinPercent call is optimal and expected
    pm.skinPercent(skin_cluster, skinned_mesh.vtx, transformValue=(joint, 1.0))

    return


def __get_shape_node( object_to_get):
    """
    Gets shape node depending on shape method
    :param object_to_get:
    :return:
    """
    if pm.objectType(object_to_get) == 'mesh':
        return object_to_get
    elif pm.objectType(object_to_get) == 'transform':
        return object_to_get.getShape()
    else:
        # edge case of catching a hierarchy object without shape past the initial param validation
        return []

def __get_skin_cluster_nodes(shape_object):
    """
    Gets skin cluster nodes
    """
    skin_cluster_node_list = shape_object.listConnections(type='skinCluster')
    return skin_cluster_node_list



def set_selected_vertex_weight_paint_influence_for_joint(selected_vertex, joint_influence, joint):
    print("Set vertex influence")

    # A selected vertex will have name format [shapeNode].vtx[i]

    vertex_list = [vertex for vertex in selected_vertex if '.vtx' in str(vertex)]

    if not vertex_list:
        print("No vertex were selected")
        # TODO: error printout
        return

    single_vertex = vertex_list[0]
    skinned_mesh_name = single_vertex.split('.vtx[')[0]
    skinned_mesh = pm.ls(skinned_mesh_name)[0]

    # TODO: deal with user selecting vertex from multiple

    shape_node = __get_shape_node(skinned_mesh)
    skin_cluster = __get_skin_cluster_nodes(shape_node)
    skin_cluster = skin_cluster[0]

    # doing a single skinPercent call is optimal and expected
    pm.skinPercent(skin_cluster, vertex_list, transformValue=(joint, joint_influence))

    return