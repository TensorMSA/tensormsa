from cluster.preprocess.preprocess_node import PreProcessNode
from master.workflow.preprocess.workflow_pre_convert import WorkFlowPreConvert as WFPreConvert

class PreProcessNodeConvert(PreProcessNode):
    """

    """

    def run(self, conf_data):
        return True


    def _init_node_parm(self, key):
        """

        :return:
        """
        wf_conf = WFPreConvert(key)
        self.batch_size = wf_conf.get_batchsize()
        self.convert_type = wf_conf.get_type()

    def _set_progress_state(self):
        pass

    def load_train_data(self, node_id, parm = 'all'):
        """
        load train data
        :param node_id:
        :param parm:
        :return:
        """
        self._init_node_parm(node_id)

        if(self.convert_type == 'seq2seq') :
            pass

    def load_test_data(self, node_id, parm = 'all'):
        """
        load test data
        :param node_id:
        :param parm:
        :return:
        """
        return []