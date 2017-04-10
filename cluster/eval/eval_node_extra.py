from cluster.eval.eval_node import EvalNode
from cluster.neuralnet.neuralnet_node_cnn import NeuralNetNodeCnn
from master import models
from cluster.common.train_summary_info import TrainSummaryInfo
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig
from common.utils import *

class EvalNodeExtra(EvalNode):
    """

    """

    def run(self, conf_data):
        """
        executed on cluster run
        :param conf_data:
        :return:
        """
        try:
            net_node = self.get_prev_node(grp='netconf')
            data_node = self.get_prev_node(grp='preprocess')
            self._init_node_parm(conf_data['node_id'])
            result = TrainSummaryInfo(type=self.eval_result_type)
            result = net_node[0].eval(conf_data['node_id'], conf_data, data=data_node, result=result)
            return result
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        netconf = WorkFlowEvalConfig(node_id)
        self.eval_result_type = netconf.get_eval_type()

    def _set_progress_state(self):
        pass