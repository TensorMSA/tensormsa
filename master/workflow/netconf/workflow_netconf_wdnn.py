from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfWdnn(WorkFlowNetConf):
    """

    """

    def __init__(self, key=None):
        """
        init key variable
        :param key::q!
        :return:
        """
        self.key = key

    def validation_check(self, json_data):
        error_msg = ""
        if ('model_path' not in json_data):
            error_msg = ''.join([error_msg, 'model_path (str) not defined'])
        if ('encoder_len' not in json_data):
            error_msg = ''.join([error_msg, 'encoder_len (int) not defined'])
        if ('decoder_len' not in json_data):
            error_msg = ''.join([error_msg, 'decoder_len (int) not defined'])
        if ('encoder_depth' not in json_data):
            error_msg = ''.join([error_msg, 'encoder_depth (int) not defined'])
        if ('decoder_depth' not in json_data):
            error_msg = ''.join([error_msg, 'decoder_depth (int) not defined'])
        if ('cell_type' not in json_data):
            error_msg = ''.join([error_msg, 'cell_type (str) (vanila, lstm, gru) not defined'])
        if ('drop_out' not in json_data):
            error_msg = ''.join([error_msg, 'drop_out (float) not defined'])
        if ('word_embed_type' not in json_data):
            error_msg = ''.join([error_msg, 'word_embed_type (str) (w2v, onehot)not defined'])
        if ('word_embed_id' not in json_data):
            error_msg = ''.join([error_msg, 'word_embed_id (str) (net id) not defined'])
        if (error_msg == ""):
            return True
        else:
            return error_msg

    def get_model_store_path(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['model_path']

    def get_encoder_len(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['encoder_len']

    def get_decoder_len(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['decoder_len']

    def get_encoder_depth(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['encoder_depth']

    def get_decoder_depth(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['decoder_depth']

    def get_cell_type(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['cell_type']

    def get_drop_out(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['drop_out']

    def get_word_embed_type(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['word_embed_type']

    def get_word_embed_id(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['word_embed_id']

    """

    """
    def validation_check(self, json_data):
        return True