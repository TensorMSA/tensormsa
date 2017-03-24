from cluster.preprocess.pre_node import PreProcessNode
import os

class PreNodeFeed(PreProcessNode):
    """

    """
    def __init__(self):
        self.pointer = 0
        self.rel = self._get_node_relation()
        data_node_name = ""
        netconf_node_name = ""


        for count in range(0 , len(self.rel['prev_grp'])) :
            if 'data' != self.rel['prev_grp'][count] :
                data_node_name = self.rel['prev'][count]
        if len(data_node_name) == 0 :
            raise Exception ("data node must be needed to use feed node")

        for count in range(0 , len(self.rel['prev_grp'])) :
            if 'netconf' != self.rel['next_grp'][count] :
                netconf_node_name = self.rel['next'][count]
        if len(data_node_name) == 0 :
            raise Exception ("netconf node must be needed to use feed node")


        cls_path, cls_name = self.get_cluster_exec_class(netconf_node_name)
        dyna_cls = self.load_class(cls_path, cls_name)
        self.input_data = dyna_cls.load_data(data_node_name, parm='all')

    def run(self, conf_data):
        pass

    def _init_node_parm(self):
        pass

    def _set_progress_state(self):
        pass

    def has_next(self):
        """
        check if hdf5 file pointer has next
        :return:
        """
        if(len(self.input_data) > self.pointer) :
            return True
        else :
            return False

    def next(self):
        """
        move pointer +1
        :return:
        """
        if(self.has_next()) :
            self.pointer = self.pointer + 1

    def __getitem__(self, key):
        """

        :param key:
        :return:
        """
        return self._convert_data_format(self.input_data[self.pointer], key)

    def _convert_data_format(self, obj, index):
        pass



