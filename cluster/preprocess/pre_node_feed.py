from cluster.preprocess.pre_node import PreProcessNode
import os

class PreNodeFeed(PreProcessNode):
    """

    """
    def run(self, conf_data):
        self.pointer = 0
        self.rel = self._get_node_relation(conf_data['nn_id'], conf_data['wf_ver'], conf_data['node_id'])
        self.cls_pool = conf_data['cls_pool']
        data_node_name = ""
        netconf_node_name = ""

        for count in range(0, len(self.rel['prev_grp'])):
            if 'data' == self.rel['prev_grp'][count]:
                data_node_name = self.rel['prev'][count]
            if 'pre_merge' == self.rel['prev_type'][count]:
                data_node_name = self.rel['prev'][count]
        if len(data_node_name) == 0:
            raise Exception("data node must be needed to use feed node")

        for count in range(0, len(self.rel['next_grp'])):
            if 'netconf' == self.rel['next_grp'][count]:
                netconf_node_name = self.rel['next'][count]
            if 'eval' == self.rel['next_grp'][count]:
                netconf_node_name = self.rel['next'][count]
        if len(netconf_node_name) == 0:
            raise Exception("netconf node must be needed to use feed node")

        self._init_node_parm(conf_data['node_id'])
        self.input_paths = self.cls_pool[data_node_name].load_data(data_node_name, parm='all')

    def _init_node_parm(self, node_id):
        pass

    def _set_progress_state(self):
        pass

    def has_next(self):
        """
        check if hdf5 file pointer has next
        :return:
        """
        if(len(self.input_paths) > self.pointer) :
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

    def file_size(self):
        """

        :return:
        """
        return len(self.input_paths)

    def __getitem__(self, key):
        """

        :param key:
        :return:
        """
        return self._convert_data_format(self.input_paths[self.pointer], key)

    def _convert_data_format(self, obj, index):
        pass

    def data_size(self):
        pass



