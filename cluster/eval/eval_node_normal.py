from cluster.eval.eval_node import EvalNode
from cluster.common.train_summary_info import TrainSummaryInfo
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig
from master.network.nn_common_manager import NNCommonManager
from master import serializers
import logging

class EvalNodeNormal(EvalNode):
    """

    """

    def run(self, conf_data):
        """
        executed on cluster run
        :param conf_data:
        :return:
        """
        try:
            logging.info("EvalNodeNormal Xgboost Run called")
            # get related nodes
            return None
        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def _init_node_parm(self, node_id):
        netconf = WorkFlowEvalConfig(node_id)
        self.eval_result_type = netconf.get_eval_type()

    def _set_progress_state(self):
        pass