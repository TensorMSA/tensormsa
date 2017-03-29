from cluster.eval.eval_node import EvalNode
from cluster.neuralnet.neuralnet_node_cnn import NeuralNetNodeCnn
from master import models
from common.utils import *

class EvalNodeExtra(EvalNode):
    """

    """

    def run(self, conf_data):
        println("run EvalNodeExtra")
        result = ""
        # result = NeuralNetNodeCnn().eval_cnn(conf_data)
        return result

    def _init_node_parm(self):
        pass

    def _set_progress_state(self):
        pass