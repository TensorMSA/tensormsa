from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfSeq2Seq(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key::q!
        :return:
        """
        self.key = key

    def validation_check(self, json_data):
        return True

    def get_model_store_path(self):
        """

        :param node_id:
        :return:
        """
        object = self.get_view_obj(self.key)
        return object['model_path']