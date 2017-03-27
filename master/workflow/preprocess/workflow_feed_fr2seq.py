from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedFr2Seq(WorkFlowPre):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key

    def validation_check(self, json_data):
        error_msg = ""
        if('encode_column' not in json_data) :
            error_msg = ''.join([error_msg, 'encode_column not defined'])
        if('decode_column' not in json_data) :
            error_msg = ''.join([error_msg, 'decode_column not defined'])
        if ('max_sentence_len' not in json_data):
            error_msg = ''.join([error_msg, 'max_sentence_len not defined'])
        if ('preprocess' not in json_data):
            error_msg = ''.join([error_msg, 'preprocess not defined'])
        if(error_msg == "") :
            return True
        else :
            raise Exception(error_msg)

    def get_encode_column(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['encode_column']

    def get_decode_column(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['decode_column']

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