from master.workflow.netconf.workflow_netconf import WorkFlowNetConf

class WorkFlowNetConfFastText(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key::q!
        :return:
        """
        if key is not None :
            self.key = key
            self.conf = self.get_view_obj(key)
        self._set_key_parms([])
        self._set_prhb_parms([])

    def set_conf_data(self, input_data):
        """
        set cofn parms for fasttext on database
        :return: dict (input data)
        """
        return self.set_view_obj(self.key, input_data)

    def get_conf_data(self):
        """
        get selected node_id's conf info
        :return: dict (conf info)
        """
        return self.get_view_obj(self.key)

    @property
    def model_store_path(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("model_path")

    @property
    def window_size(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("window_size")

    @property
    def vector_size(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("vector_size")

    @property
    def vector_size(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("batch_size")

    @property
    def iter(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("iter")

    @property
    def min_count(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("min_count")

    @property
    def preprocess(self):
        """
        getter for wide and cnn
        :return:s
        """
        return self.conf.get("preprocess")