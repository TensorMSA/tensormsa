from cluster.data.data_node import DataNode
import h5py
import numpy as np

class DataNodeFrame(DataNode):
    """

    """

    def run(self, conf_data):
        return None

    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def load_train_data(self, node_id, parm = 'all'):
        return []

    def load_test_data(self, node_id, parm = 'all'):
        return []