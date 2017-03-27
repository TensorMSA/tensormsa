from __future__ import absolute_import, unicode_literals

from celery import shared_task
from master import models
from cluster.common.common_node import WorkFlowCommonNode

@shared_task
def train(nn_id, wf_ver) :
    print ("[Train Task] Start Celery Job ")
    result = WorkFlowTrainTask()._exec_train(nn_id, wf_ver)
    return result

class WorkFlowTrainTask(WorkFlowCommonNode):
    """

    """
    def _exec_train(self, nn_id, wf_ver):
        """
        start train with predefined workflow process
        :param nn_id:
        :param wf_ver:
        :return:
        """
        try :
            self.nn_id = nn_id
            self.wf_ver = wf_ver

            # get node sequece list
            node_list = self._get_arranged_node_list()
            if(len(node_list) == 0) :
                return None

            cls_list = self._get_cached_class_pool(node_list)

            # execute nodes by sequece
            result_info = []
            for node in node_list :
                _relation = self._get_node_relation(nn_id, wf_ver, node)
                conf_data = {}
                conf_data['node_id'] = node
                conf_data['node_list'] = node_list
                conf_data['node_prev'] = _relation['prev']
                conf_data['node_next'] = _relation['next']
                conf_data['nn_id'] = nn_id
                conf_data['wf_ver'] = wf_ver
                conf_data['cls_pool'] = cls_list
                result_info.append(cls_list[node].run(conf_data))
            return result_info
        except Exception as e :
            raise Exception (e)

    def _get_arranged_node_list(self):
        """
        get sequence of nodes to execute
        :return:
        """
        return_arr = []
        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=self.nn_id + "_" + self.wf_ver)
        for data in query_set:
            if(len(return_arr) == 0) :
                return_arr.append(data.nn_wf_node_id_1)
                return_arr.append(data.nn_wf_node_id_2)
            else :
                if((data.nn_wf_node_id_1 in return_arr) and return_arr.index(data.nn_wf_node_id_1) >= 0) :
                    idx = return_arr.index(data.nn_wf_node_id_1)
                    return_arr.insert(idx + 1, data.nn_wf_node_id_2)
                elif((data.nn_wf_node_id_2 in return_arr) and return_arr.index(data.nn_wf_node_id_2) >= 0) :
                    idx = return_arr.index(data.nn_wf_node_id_2)
                    return_arr.insert(idx, data.nn_wf_node_id_1)
        return return_arr

    def _get_cached_class_pool(self, node_name_list):
        """

        :param node_name_list:
        :return:
        """
        try :
            class_list = {}
            for node in node_name_list :
                _path, _cls = self.get_cluster_exec_class(node)
                class_list[node] = self.load_class(_path, _cls)
            return class_list
        except Exception as e :
            raise Exception (e)

    def _run_next_node(self):
        return None

    def _check_node_job_state(self):
        return None

    def _report_server_state(self):
        return None

    def _report_job_state(self):
        return None


