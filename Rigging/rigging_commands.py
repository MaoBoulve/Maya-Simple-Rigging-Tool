import rigging_tasks

class BackEndCommands:
    """
    Command class for functions involving data handling of rigging tasks
    """

    class WeightPainting:
        # TODO: save class variables in metadata instead

        _weight_paint_joint = None
        _mesh_to_paint = None
        _vertex_list_to_paint = []

        @classmethod
        def set_weight_paint_joint(cls, new_joint):
            cls._weight_paint_joint = new_joint
            return

        @classmethod
        def set_mesh_to_paint(cls, new_mesh):
            cls._mesh_to_paint = new_mesh
            return

        @classmethod
        def set_vertex_list_to_paint(cls, vertex_list):
            cls._vertex_list_to_paint = vertex_list
            return

        @classmethod
        def apply_mesh_weight_paint(cls, weight_paint_value):
            rigging_tasks.set_mesh_weight_paint_influence_from_joint(skinned_mesh=cls._mesh_to_paint,
                                                                     joint_influence=weight_paint_value,
                                                                     joint=cls._weight_paint_joint)
            return

        @classmethod
        def apply_vertex_weight_paint(cls, weight_paint_value):
            rigging_tasks.set_vertex_weight_paint_influence_from_joint(selected_vertex=cls._vertex_list_to_paint,
                                                                       joint_influence=weight_paint_value,
                                                                       joint=cls._weight_paint_joint)
            return

class FrontEndCommands:
    """
    Command class for drawing UI and any other Qt visual handling
    """