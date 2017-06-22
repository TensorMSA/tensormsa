from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfW2V(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key::q!
        :return:
        """
        self.key = key
        self._set_key_parms(['window_size', 'window_size', 'vector_size', 'batch_size', 'iter', 'min_count'])
        self._set_prhb_parms(['window_size', 'vector_size'])

    def get_model_store_path(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('model_path')

    def get_window_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('window_size')

    def get_vector_size(self):
        """

        :param node_id:
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('vector_size')

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
        return self.conf.get('iter')

    def get_min_count(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return 1 if self.conf.get('min_count') is None else self.conf.get('min_count')

    def preprocess_type(self):
        """

        :param node_id:
        :return:
        """
        if ('conf' not in self.__dict__):
            self.conf = self.get_view_obj(self.key)
        return 'mecab' if self.conf.get('preprocess') is None else self.conf.get('preprocess')