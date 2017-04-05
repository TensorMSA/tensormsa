from cluster.preprocess.pre_node import PreProcessNode
import os

class PreNodeFeed(PreProcessNode):
    """
    Error check rule add : Dataconf Add

    """
    def run(self, conf_data):
        self.pointer = 0
        data_node_cls = None
        netconf_node_cls = None

        prev_node_list = self.get_prev_node()
        for prev_node in prev_node_list:
            if 'data' == prev_node.get_node_grp():
                data_node_cls = prev_node
            if 'pre_merge' == prev_node.get_node_type():
                data_node_cls = prev_node
            if 'dataconf' == prev_node.get_node_grp():
                data_node_cls = prev_node
        if data_node_cls == None:
            raise Exception("data node must be needed to use feed node")

        next_node_list = self.get_next_node()
        for next_node in next_node_list:
            if 'netconf' == next_node.get_node_grp():
                netconf_node_cls = next_node
            if 'eval' == next_node.get_node_grp():
                netconf_node_cls = next_node
        if netconf_node_cls == None :
            raise Exception("netconf node must be needed to use feed node")

        self.input_paths = data_node_cls.load_data(data_node_cls.get_node_name(), parm='all')

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

    def reset_pointer(self):
        """
        check if hdf5 file pointer has next
        :return:
        """
        self.pointer = 0

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



