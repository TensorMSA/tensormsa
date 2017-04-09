from cluster.neuralnet.neuralnet_node import NeuralNetNode
from master.workflow.netconf.workflow_netconf_autoencoder import WorkFlowNetConfAutoEncoder
import tensorflow as tf
import numpy as np

class NeuralNetNodeAutoEncoder(NeuralNetNode):
    """

    """

    def run(self, conf_data):
        try:
            # init parms
            self._init_node_parm(conf_data['node_id'])
            self.cls_pool = conf_data['cls_pool']
            return None
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        wf_conf = WorkFlowNetConfAutoEncoder(node_id)

    def _set_progress_state(self):
        return None

    def predict(self, node_id, parm = {}):
        pass

    def eval(self, node_id, parm={}):
        """

        :param node_id:
        :param parm:
        :return:
        """
        pass