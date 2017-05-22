from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models

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
        self._set_prhb_parms(['encoder_len', 'decoder_len', 'cell_type', 'word_embed_type', 'word_embed_id'])

    def validation_check(self, json_data):
        error_msg = ""
        if('encoder_len' not in json_data) :
            error_msg = ''.join([error_msg, 'encoder_len (int) not defined'])
        if('decoder_len' not in json_data) :
            error_msg = ''.join([error_msg, 'decoder_len (int) not defined'])
        if('encoder_depth' not in json_data) :
            error_msg = ''.join([error_msg, 'encoder_depth (int) not defined'])
        if('decoder_depth' not in json_data):
            error_msg = ''.join([error_msg, 'decoder_depth (int) not defined'])
        if('cell_type' not in json_data):
            error_msg = ''.join([error_msg, 'cell_type (str) (vanila, lstm, gru) not defined'])
        if('drop_out' not in json_data):
            error_msg = ''.join([error_msg, 'drop_out (float) not defined'])
        if('word_embed_type' not in json_data):
            error_msg = ''.join([error_msg, 'word_embed_type (str) (w2v, onehot)not defined'])
        if('word_embed_id' not in json_data):
            error_msg = ''.join([error_msg, 'word_embed_id (str) (net id) not defined'])
        if('cell_size' not in json_data):
            error_msg = ''.join([error_msg, 'cell_size (int) not defined'])
        if ('batch_size' not in json_data):
            error_msg = ''.join([error_msg, 'batch_size (int) not defined'])
        if ('iter' not in json_data):
            error_msg = ''.join([error_msg, 'iter (int) not defined'])
        if ('early_stop' not in json_data):
            error_msg = ''.join([error_msg, 'eary_stop (int) not defined'])
        if ('learning_rate' not in json_data):
            error_msg = ''.join([error_msg, 'learning_rate (int) not defined'])
        if(error_msg == "") :
            return True
        else :
            raise Exception (error_msg)

    def get_model_store_path(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('model_path')

    def get_encoder_len(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('encoder_len')

    def get_decoder_len(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('decoder_len')

    def get_encoder_depth(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('encoder_depth')

    def get_decoder_depth(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('decoder_depth')

    def get_cell_type(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('cell_type')

    def get_drop_out(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('drop_out')

    def get_word_embed_type(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('word_embed_type')

    def get_word_embed_id(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('word_embed_id')

    def get_cell_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('cell_size')

    def get_batch_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('batch_size')

    def get_iter_size(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['iter']

    def get_early_stop_stand(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('early_stop')

    def get_learn_rate(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('learning_rate')

    def get_vocab_size(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('vocab_size')

    def set_vocab_size(self, data):
        """

        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data['vocab_size'] = data
        obj.save()

    def set_vocab_list(self, data, id='vocab_list'):
        """

        :param node_id:
        :return:
        """
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
        config_data = getattr(obj, 'node_config_data')
        config_data[id] = data
        obj.save()

    def get_vocab_list(self, id='vocab_list'):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get(id)