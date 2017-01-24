
class WorkFlowPre :

    def get_node_status(self):
        """
        return node status info (nn_id, nn_ver, node_type, node_prg, etc)
        :return:
        """
        return None

    def get_related_node_status(self):
        """
        get related node info (especially data node)
        :return:object (related node's data info)
        """
        return None

    def get_view_obj(self):
        """
        get column type info for view
        :return:
        """
        pass

    def set_view_obj(self, obj):
        """
        set column type info on db json filed
        :param obj:
        :return:
        """
        pass