from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedFr2Auto(WorkFlowPre):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms([])
        self._set_prhb_parms([])

    def get_encode_column(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['encode_column']

    def get_encode_len(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['encode_len']

    def get_preprocess_type(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['preprocess']