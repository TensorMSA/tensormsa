from __future__ import absolute_import, unicode_literals
import importlib
from celery import shared_task
from cluster.common.common_node import WorkFlowCommonNode

@shared_task
def single_run(nn_id, wf_ver, node) :
    print ("[Train Task] Start Celery Job ")
    result = WorkFlowSingleTask()._run_single_node(nn_id, wf_ver, node)
    return result


class WorkFlowSingleTask(WorkFlowCommonNode):

    def _run_single_node(self, nn_id, wf_ver, node):
        """
        run given single node directly and return result
        :param obj: nn_id, ver, node and etc
        :return:
        """
        try:
            self.nn_id = nn_id
            self.wf_ver = wf_ver
            node_id = nn_id + '_' + wf_ver + '_' + node
            result_info = []
            # execute nodes by sequece
            # 밑져야 본전이니 전화 후는 그 들고 있자.

            _relation = self._get_node_relation(nn_id, wf_ver, node_id)
            _path, _cls = self.get_cluster_exec_class(node_id)
            conf_data = {}
            conf_data['node_id'] = node_id
            conf_data['node_list'] = None
            conf_data['node_prev'] = _relation['prev']
            conf_data['node_next'] = _relation['next']
            conf_data['nn_id'] = nn_id
            conf_data['wf_ver'] = wf_ver
            result_info.append(self.load_class(_path, _cls).run(conf_data))

            return result_info
        except Exception as e:
            raise Exception(e)