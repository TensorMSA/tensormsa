import importlib
from django.db import connection
from common.utils import *
from master import models

class WorkFlowCommonNode :
    """

    """
    def run(self, conf_data):
        pass

    def _init_node_parm(self):
        pass

    def _set_progress_state(self):
        pass

    def find_prev_node(self, node_name, node_list):
        """
        find prev node and return name
        :param node_name:
        :param node_list:
        :return:
        """
        if(node_list.index(node_name) > 0) :
            return node_list[node_list.index(node_name) - 1]
        else :
            raise Exception ('no prev node available')

    def find_next_node(self, node_name, node_list):
        """
        find next node and return name
        :param node_name:
        :param node_list:
        :return:
        """
        if(node_list.index(node_name) < len(node_list)) :
            return node_list[node_list.index(node_name) + 1]
        else :
            raise Exception ('no next node available')


    def get_cluster_exec_class(self, node_id):
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

    def load_class(self, class_path, class_name):
        """
        return class with name
        :param module_name:
        :param class_name:
        :return: Class
        """

        module = importlib.import_module(class_path)
        LoadClass = getattr(module, class_name)
        print("Execute Node Name : {0} ".format(LoadClass))
        return LoadClass()

    def _get_node_relation(self, nn_id, wf_ver, node_id):
        """
        get node relations connected with selected node_id
        :return:
        """
        return_obj = {}
        prev_arr = []
        next_arr = []

        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=nn_id + "_" + wf_ver)

        for data in query_set:
            if(node_id == data.nn_wf_node_id_2) :
                prev_arr.append(data.nn_wf_node_id_1)
            if (node_id == data.nn_wf_node_id_1):
                next_arr.append(data.nn_wf_node_id_2)

        return_obj['prev'] = prev_arr
        return_obj['next'] = next_arr

        return return_obj

