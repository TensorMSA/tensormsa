from master.workflow.preprocess.workflow_pre import WorkFlowPre
from master import models

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
        return self.conf.get('encode_column')

    def get_encode_len(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('encode_len')

    def get_preprocess_type(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('preprocess')

    def set_vocab_list(self, data):
        """

        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['vocab_list'] = data
        obj.save()

    def get_vocab_list(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('vocab_list')

    def get_vocab_size(self):
        """
        get vocab size for onhot encoder
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('vocab_size')

    def get_embed_type(self):
        """
        get vector embed type
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('embed_type')