from master.workflow.preprocess.workflow_pre import WorkFlowPre
from master import models

class WorkflowFeedFr2Wcnn(WorkFlowPre):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if key is not None :
            self.key = key
            self.conf = self.get_view_obj(key)
        self._set_key_parms([])
        self._set_prhb_parms([])

    def set_vocab_list(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['vocab_list'] = data
        obj.save()

    def set_lable_list(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['lable_list'] = data
        obj.save()

    def set_word_vector_size(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['word_vector_size'] = data
        obj.save()

    def set_char_embed(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['char_embed'] = data
        obj.save()

    def set_char_max_len(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['char_max_len'] = data
        obj.save()

    def set_encode_len(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['encode_len'] = data
        obj.save()

    def set_encode_channel(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['encode_channel'] = data
        obj.save()

    def set_char_embed_size(self, data):
        """
        setter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['char_embed_size'] = data
        obj.save()

    @property
    def get_encode_column(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['encode_column']

    @property
    def get_encode_channel(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['channel']

    @property
    def get_encode_len(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['encode_len']

    @property
    def get_decode_column(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['decode_column']

    @property
    def get_lable_size(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['lable_size']

    @property
    def get_preprocess_type(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['preprocess']

    @property
    def char_embed_flag(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf.get('char_embed')

    @property
    def get_lable_list(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf.get('lable_list')

    @property
    def get_vocab_size(self):
        """
        get vocab size for onhot encoder
        :return:
        """
        return self.conf.get('vocab_size')

    @property
    def get_embed_type(self):
        """
        get vector embed type
        :return:
        """
        return self.conf.get('embed_type')

    @property
    def get_lable_list(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return self.conf.get("lable_list")

    @property
    def get_vocab_list(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return self.conf.get("vocab_list")

    @property
    def char_encode(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return_val = self.conf.get('char_encode')
        return False if return_val == None else return_val

    @property
    def char_max_len(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return_val = self.conf.get('char_max_len')
        return 5 if return_val == None else return_val