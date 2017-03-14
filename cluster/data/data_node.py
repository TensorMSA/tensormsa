from cluster.common.common_node import WorkFlowCommonNode

class DataNode(WorkFlowCommonNode):
    """

    """

    def run(self, conf_data):
        pass

    def _init_node_parm(self, node_id):
        pass

    def _set_progress_state(self):
        pass

    def load_train_data(self, node_id, parm = 'all'):
        pass

    def load_test_data(self, node_id, parm = 'all'):
        pass