from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models
from common.utils import *

class WorkFlowNetConfWideCnn(WorkFlowNetConf):
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

    @property
    def vocab_size(self):
        """
        getter for wide and cnn
        :param node_id:
        :return:
        """
        return self.conf.get('vocab_size')

    @property
    def char_embed(self):
        """
        getter for wide and cnn
        :param node_id:
        :return:
        """
        return self.conf.get('char_embed')

    @property
    def num_classes(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("config").get("num_classes")

    @property
    def learnrate(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("config").get("learnrate")

    @property
    def layeroutputs(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("config").get("layeroutputs")

    @property
    def out(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("out")

    @property
    def epoch(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("param").get("epoch")

    @property
    def batch_size(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("param").get("batch_size")

    @property
    def labels(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("labels")

    @property
    def modelname(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("modelname")

    @property
    def traincnt(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("param").get("traincnt")

    @property
    def model_path(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("model_path")

    @property
    def type(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("config").get("type")

    @property
    def predictcnt(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("param").get("predictcnt")

    @property
    def get_layer_info(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("layers")

    @property
    def get_lable_list(self):
        """

        :param node_id:
        :return:
        """
        return self.conf.get("lable_list")

    @property
    def get_vocab_list(self):
        """

        :param node_id:
        :return:
        """
        return self.conf.get("vocab_list")

    @property
    def encode_column(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['encode_column']

    @property
    def encode_channel(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['channel']

    @property
    def get_decode_column(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['decode_column']

    @property
    def lable_size(self):
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
    def get_vocab_size(self):
        """
        get vocab size for onhot encoder
        :return:
        """
        return self.conf.get('vocab_size')

    @property
    def word_vector_size(self):
        """
        get vocab size for onhot encoder
        :return:
        """
        return self.conf.get('word_vector_size')

    @property
    def encode_len(self):
        """
        getter for WorkflowFeedFr2Wcnn conf
        :param node_id:
        :return:
        """
        return self.conf['encode_len']

    @property
    def embed_type(self):
        """
        get vector embed type
        :return:
        """
        return self.conf.get('embed_type')

    @property
    def get_vocab_list(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return self.conf.get("vocab_list")

    @property
    def get_lable_list(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return self.conf.get("lable_list")

    @property
    def lable_onehot(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        lable_onehot = OneHotEncoder(self.lable_size)
        if (self.get_lable_list):
            lable_onehot.restore(self.get_lable_list)
        return lable_onehot

    @property
    def input_onehot(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        input_onehot = OneHotEncoder(self.vocab_size + 4)
        if (self.get_vocab_list):
            input_onehot.restore(self.get_vocab_list)
        return input_onehot

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

    @property
    def char_embed_size(self):
        """
        get vector embed type
        :param node_id:
        :return:
        """
        return_val = self.conf.get('char_embed_size')
        return 160 if return_val == None else return_val
