from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfD2V(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key::q!
        :return:
        """
        self.key = key
        self._set_prhb_parms(['model_path', 'window_size', 'vector_size' ])

    def validation_check(self, json_data):
        error_msg = ""
        if ('model_path' not in json_data):
            error_msg = ''.join([error_msg, 'model_path (str) not defined'])
        if ('window_size' not in json_data):
            error_msg = ''.join([error_msg, 'window_size (int) not defined'])
        if ('vector_size' not in json_data):
            error_msg = ''.join([error_msg, 'vector_size (int) not defined'])
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
        return self.conf['model_path']

    def get_window_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['window_size']

    def get_vector_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['vector_size']

    def get_batch_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['batch_size']

    def get_iter_size(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return self.conf['iter']