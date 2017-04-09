from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkFlowPreMerge(WorkFlowPre):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms(['batchsize', 'merge_rule', 'type'])
        self._set_prhb_parms([])

    def get_batchsize(self):
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['batchsize']

    def get_merge_rule(self):
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['merge_rule']

    def get_type(self):
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['type']

    def get_state_code(self):
        if('state_id' not in self.__dict__) :
            self.state_id = self.get_state_id(self.key)
        return self.state_id

