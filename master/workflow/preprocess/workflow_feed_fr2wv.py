from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedFr2Wv(WorkFlowPre):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms(['col_list', 'max_sentence_len', 'preprocess'])
        self._set_prhb_parms(['col_list', 'max_sentence_len', 'preprocess'])

    def get_column_list(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['col_list']

    def get_sent_max_len(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['max_sentence_len']

    def get_preprocess_type(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['preprocess']