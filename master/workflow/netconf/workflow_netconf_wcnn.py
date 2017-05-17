from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models

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
    def batch_size(self):
        """
        getter for wide and cnn
        :return:
        """
        return self.conf.get("config").get("num_classes")

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

