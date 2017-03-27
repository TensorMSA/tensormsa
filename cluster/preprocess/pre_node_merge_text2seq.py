from cluster.preprocess.pre_node import PreProcessNode
from master.workflow.preprocess.workflow_pre_merge import WorkFlowPreMerge as WFPreMerge

class PreNodeMergeText2Seq(PreProcessNode):
    """

    """

    def run(self, conf_data):
        return True


    def _init_node_parm(self, key):
        """

        :return:
        """
        wf_conf = WFPreMerge(key)
        self.batch_size = wf_conf.get_batchsize()
        self.merge_rule = wf_conf.get_merge_rule()
        self.merge_type = wf_conf.get_type()
        self.state_code = wf_conf.get_state_code()

    def _set_progress_state(self):
        pass

    def load_data(self, node_id, parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        self._init_node_parm(node_id)

        if(self.merge_type == 'seq2seq') :
            return self._merge_seq2seq_type()
        else :
            raise Exception ("merge node error: not defined type {0}".format(self.merge_type))

    def _merge_seq2seq_type(self):
        """
        merge two data node into one for seq2seq anal
        :return:
        """
        file_lists = []
        encode_data = []
        encode_node_list = self.merge_rule['encode_node']
        if (len(encode_node_list) > 0):
            for node_name in encode_node_list:
                cls_path, cls_name = self.get_cluster_exec_class(str(self.state_code) + "_" + node_name)
                dyna_cls = self.load_class(cls_path, cls_name)
                encode_data = encode_data + dyna_cls.load_data(self.state_code + "_" + node_name, parm='all')
        file_lists.append(encode_data)

        decode_data = []
        decode_node_list = self.merge_rule['decode_node']
        if (len(decode_node_list) > 0):
            for node_name in decode_node_list:
                cls_path, cls_name = self.get_cluster_exec_class(self.state_code + "_" + node_name)
                dyna_cls = self.load_class(cls_path, cls_name)
                decode_data = decode_data + dyna_cls.load_data(self.state_code + "_" + node_name, parm='all')
        file_lists.append(decode_data)

        return file_lists