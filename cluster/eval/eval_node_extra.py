from cluster.eval.eval_node import EvalNode
from cluster.common.train_summary_info import TrainSummaryInfo
from master.workflow.evalconf.workflow_evalconf import WorkFlowEvalConfig
from master.network.nn_common_manager import NNCommonManager
from master import serializers
import logging

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
            # get related nodes
            net_node = self.get_prev_node(grp='netconf')
            data_node = self.get_prev_node(grp='preprocess')
            self._init_node_parm(conf_data['node_id'])

            # set result info cls
            result = TrainSummaryInfo(type=self.eval_result_type)
            result.set_nn_wf_ver_id(conf_data['wf_ver'])
            result.set_nn_id(conf_data['nn_id'])

            # run eval for each network
            result = net_node[0].eval(conf_data['node_id'], conf_data, data=data_node[0], result=result)

            if result is None or result == '':
                return {}
            # set parms for db store
            input_data = TrainSummaryInfo.save_result_info(self, result)
            input_data['accuracy'] = result.get_accuracy()

            condition_data = {}
            condition_data['nn_wf_ver_id'] = conf_data['wf_ver']
            condition_data['condition'] = "3"  # 1 Pending, 2 Progress, 3 Finish, 4 Error
            # Net Version create
            NNCommonManager().update_nn_wf_info(conf_data['nn_id'], condition_data)

            return input_data
        except Exception as e:
            condition_data = {}
            condition_data['nn_wf_ver_id'] = conf_data['wf_ver']
            condition_data['condition'] = "4"  # 1 Pending, 2 Progress, 3 Finish, 4 Error
            # Net Version create
            NNCommonManager().update_nn_wf_info(conf_data['nn_id'], condition_data)
            logging.error(e)
            raise Exception(e)

    def _init_node_parm(self, node_id):
        netconf = WorkFlowEvalConfig(node_id)
        self.eval_result_type = netconf.get_eval_type()

    def _set_progress_state(self):
        pass