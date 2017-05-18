from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models

class WorkFlowNetConfAutoEncoder(WorkFlowNetConf):
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

    def validation_check(self, json_data):
        error_msg = ""
        if ('learning_rate' not in json_data):
            error_msg = ''.join([error_msg, 'learning_rate (int) not defined'])
        if ('batch_size' not in json_data):
            error_msg = ''.join([error_msg, 'batch_size (int) not defined'])
        if ('batch_size' not in json_data):
            error_msg = ''.join([error_msg, 'batch_size (int) not defined'])
        if ('iter' not in json_data):
            error_msg = ''.join([error_msg, 'iter (int) not defined'])
        if (error_msg == ""):
            return True
        else:
            raise Exception (error_msg)

    def get_model_store_path(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('model_path')

    def get_iter_size(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['iter']

    def get_batch_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['batch_size']

    def get_learn_rate(self):
        """
        get learning rate of autoencoder
        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('learning_rate')

    def get_n_input(self):
        """
        number of autoencoder input vecotr size
        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('input_size')

    def get_n_hidden(self):
        """
        number of autoencoder hidden layer size
        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('n_hidden')

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

    def get_input_len(self):
        """
        get vector embed type
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('input_size')

    def get_feeder_pre_type(self):
        """
        get vector embed type
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('preprocess_type')

    def get_feeder_column_encoder(self):
        """
        get vector embed type
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('encode_onehot')

    def get_encode_dtype(self):
        """
        get vector embed type
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('encode_dtype')
