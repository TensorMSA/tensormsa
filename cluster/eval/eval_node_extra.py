from cluster.eval.eval_node import EvalNode
from cluster.neuralnet.neuralnet_node_cnn import NeuralNetNodeCnn
from master import models
from common.utils import *

class EvalNodeExtra(EvalNode):
    """

    """

    def run(self, conf_data):
        println("run EvalNodeExtra")
        try:
            self.cls_pool = conf_data['cls_pool']
            net_node_name = self._get_backward_node_with_type(conf_data['node_id'], 'netconf')
            net_node = self.cls_pool[net_node_name[0]]
            result = net_node.eval(conf_data['node_id'],conf_data)
            return result
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self):
        pass

    def _set_progress_state(self):
        pass