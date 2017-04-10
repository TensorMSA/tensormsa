from cluster.eval.eval_node import EvalNode
from cluster.neuralnet.neuralnet_node_cnn import NeuralNetNodeCnn
from master import models
from cluster.common.train_summary_info import TrainSummaryInfo
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig
from common.utils import *
from master import serializers

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
            input_data = {}
            input_data['nn_id'] = result.get_nn_id()
            input_data['nn_wf_ver_id'] = result.get_nn_wf_ver_id()
            input_data['nn_batch_ver_id'] = 1
            input_data['result_info'] = result.get_result_info()
            serializer = serializers.TRAIN_SUMMARY_RESULT_INFO_Serializer(data=input_data)
            if serializer.is_valid():
                serializer.save()
            return input_data['result_info']
        except Exception as e:
            raise Exception(e)

    def _init_node_parm(self, node_id):
        netconf = WorkFlowEvalConfig(node_id)
        self.eval_result_type = netconf.get_eval_type()

    def _set_progress_state(self):
        pass