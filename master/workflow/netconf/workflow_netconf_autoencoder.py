from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

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

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('learning_rate')

    def get_n_input(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('n_input')

    def get_n_hidden(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('n_hidden')