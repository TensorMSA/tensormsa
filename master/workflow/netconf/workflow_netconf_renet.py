from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfReNet(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key::q!
        :return:
        """
        self.key = key
        self._set_essence_parms([])
        self._set_update_prohibited_ids([])

    def get_model_store_path(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['model_path']