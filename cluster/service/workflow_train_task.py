from __future__ import absolute_import, unicode_literals
import importlib
from celery import shared_task
from master import models
from django.core import serializers as serial
from django.db import connection
from common.utils import dictfetchall
from common.utils import *

@shared_task
def train(nn_id, wf_ver) :
    print ("[Train Task] Start Celery Job ")
    result = WorkFlowTrainTask()._exec_train(nn_id, wf_ver)
    return result

class WorkFlowTrainTask():
    """

    """
    def _exec_train(self, nn_id, wf_ver):
        """
        start train with predefined workflow process
        :param nn_id:
        :param wf_ver:
        :return:
        """
        self.nn_id = nn_id
        self.wf_ver = wf_ver

        # get node sequece list
        node_list = self._get_arranged_node_list()
        if(len(node_list) == 0) :
            return None

        println(node_list)
        # execute nodes by sequece
        for node in node_list :
            _path, _cls = self._get_cluster_exec_class(node)
            obj = self._load_class(_path, _cls).run(node)
            println(_path)
            println(_cls)
            println(obj)

        return {}

    def _load_class(self, class_path, class_name):
        """
        return class with name
        :param module_name:
        :param class_name:
        :return: Class
        """

        module = importlib.import_module(class_path)
        LoadClass = getattr(module, class_name)

        return LoadClass()

    def _get_arranged_node_list(self):
        """
        get sequence of nodes to execute
        :return:
        """
        return_arr = []
        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=self.nn_id + "_" + self.wf_ver)
        for data in query_set:
            print(data)
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

    def _get_cluster_exec_class(self, node_id):
        """
        get execute class path
        :param node_id:
        :return:
        """
        # make query string (use raw query only when cate is too complicated)
        query_list = []
        query_list.append("SELECT wf_node_class_name, wf_node_class_path ")
        query_list.append("FROM  master_NN_WF_NODE_INFO ND JOIN master_WF_TASK_SUBMENU_RULE SB   ")
        query_list.append("      ON ND.wf_task_submenu_id_id =  SB.wf_task_submenu_id  ")
        query_list.append("WHERE ND.nn_wf_node_id = %s")

        # parm_list : set parm value as list
        parm_list = []
        parm_list.append(node_id)

        with connection.cursor() as cursor:
            cursor.execute(''.join(query_list), parm_list)
            row = dictfetchall(cursor)
        return row[0]['wf_node_class_path'], row[0]['wf_node_class_name']

    def _run_next_node(self):
        return None

    def _check_node_job_state(self):
        return None

    def _report_server_state(self):
        return None

    def _report_job_state(self):
        return None


