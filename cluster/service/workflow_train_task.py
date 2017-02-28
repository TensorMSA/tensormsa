from __future__ import absolute_import, unicode_literals
import importlib
from celery import shared_task
from master import models
from common.utils import *

@shared_task
def train(input_data) :
    println ("[Train Task] Start Celery Job ")
    nn_id = input_data["key"]["nn_id"]
    wf_ver_id = input_data["key"]["wf_ver_id"]
    node_id = input_data["key"]["node_id"]

    result = WorkFlowTrainTask()._exec_train(nn_id, wf_ver_id, node_id)
    return result

class WorkFlowTrainTask():
    """

    """
    def _exec_train(self, nn_id, wf_ver_id, node_id):
        """
        start train with predefined workflow process
        :param nn_id:
        :param wf_ver:
        :return:
        """
        println("WorkFlowTrainTask")
        self.nn_id = nn_id
        println(nn_id)
        self.wf_ver_id = wf_ver_id
        println(wf_ver_id)
        self.node_id = node_id
        println(node_id)
        self._get_arranged_node_list()
        println("_get_arranged_node_list end")

        # # get next node id to run
        # _node_id = self._get_next_node(nn_id, wf_ver_id)
        # if(_node_id == None) :
        #     return
        # # get node info (class name & class run config info)
        # _cls, _cls_data = self._get_node_info(_node_id)
        # # run node
        # step_result = self._load_class(_cls).run(_cls_data)
        # # run next
        # self._exec_train(nn_id, wf_ver_id)



    def _get_next_node(self, nn_id, wf_ver_id):
        node_id = None
        return node_id

    def _get_node_info(self, node_id):
        _cls = None
        _cls_data = None
        return _cls, _cls_data

    def _get_module_name(self, type):
        if(type == 'DATA'):
            return "cluster.data"
        elif(type == 'NET'):
            return "cluster.neuralnet"
        elif(type == 'PRE'):
            return "cluster.preprocess"
        elif (type == 'CONF'):
            return "cluster.dataconfig"

    def _load_class(self, class_name, type):
        """
        return class with name
        :param module_name:
        :param class_name:
        :return: Class
        """
        module = importlib.import_module(self._get_module_name(type))
        LoadClass = getattr(module, class_name)
        return LoadClass()

    def _exec_node(self):
        return None

    def _stop_task(self):
        return None

    def _get_arranged_node_list(self):
        println("call get arranged node")
        println(self.nn_id)
        println(self.wf_ver_id)
        return_arr = []
        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=self.nn_id + "_" + self.wf_ver_id)
        for data in query_set:

            println(data.nn_wf_node_id_1)
            println(data.nn_wf_node_id_2)
            println(type(data))
        return None

    def _run_next_node(self):
        return None

    def _check_node_job_state(self):
        return None

    def _report_server_state(self):
        return None

    def _report_job_state(self):
        return None


