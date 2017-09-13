from __future__ import absolute_import, unicode_literals
from django.db import connection
from celery import shared_task
from master import models
from cluster.common.common_node import WorkFlowCommonNode
from common.utils import *
import logging
from logging import FileHandler
from django.conf import settings
import datetime


@shared_task
def train(nn_id, wf_ver) :

    log_home = "/root"
    _celery_log_dir = make_celery_dir_by_datetime(log_home)
    celery_log_dir = make_and_exist_directory(_celery_log_dir)

    celery_log_file = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _filename = str(nn_id) +"_" +str(wf_ver) +"_" +  celery_log_file + ".log"

    celery_log_file = celery_log_dir + _filename

    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger()
    task_handler = FileHandler(celery_log_file)
    logger.addHandler(task_handler)
    logging.info("=============================================================")
    logging.info("[Train Task] Start Celery Job {0} {1}".format(nn_id, wf_ver))
    logging.info("=============================================================")
    result = WorkFlowTrainTask()._exec_train(nn_id, wf_ver)
    logging.info("=============================================================")
    logging.info("[Train Task] Done Celery Job {0} {1} : {2}".format(nn_id, wf_ver, result))
    logging.info("=============================================================")
    return result

def make_celery_dir_by_datetime(home_dir):
    """ 현재시간을 사용하여 디렉토리 이름 반환
         Make Datetime directory by datetime functions

    Args:
      params:

    Returns:
        directory name using datetime

    Raises:

    Example

    """
    celery_log_dir = datetime.datetime.now().strftime('%Y-%m-%d')
    celery_work_dir = home_dir + "/"+ celery_log_dir + "/"
    return celery_work_dir


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
            node_list = self._get_all_nodes_list()
            if(len(node_list) == 0) :
                return None
            cls_list = self._get_cached_class_pool(node_list)
            node_rel_list = self._get_node_rel_data()
            node_graph_set = self._create_node_graph(node_list, cls_list, node_rel_list)
            first_node = self._find_first_node(node_graph_set)

            # execute nodes by sequece
            result_info = {}
            while True :
                search_info = self._search_next_node(first_node)
                if(search_info[0] == False) :
                    break
                first_node = search_info[1]
                if(search_info[2] != None) :
                    _relation = self._get_node_relation(nn_id, wf_ver, search_info[2].get_node_name())
                    conf_data = {}
                    conf_data['node_id'] = search_info[2].get_node_name()
                    conf_data['node_list'] = node_list
                    conf_data['node_prev'] = _relation['prev']
                    conf_data['node_next'] = _relation['next']
                    conf_data['nn_id'] = nn_id
                    conf_data['wf_ver'] = wf_ver
                    conf_data['cls_pool'] = cls_list
                    logging.info("[Node Start] {0}".format(search_info[2].node_name))
                    key = '_'.join([search_info[2].net_id, search_info[2].net_ver])
                    result_info[key] = search_info[2].run(conf_data)
                    logging.info("[Node End] {0}".format(search_info[2].node_name))
            return result_info
        except Exception as e :
            logging.error("Error on node [{0}][{1}]".format(search_info[2].node_name, e))
            raise Exception (e)

    def _search_next_node(self, graph_node):
        """

        :param linked_list:
        :return:
        """
        try :
            stop_flag = True
            next_task = None
            current_Task = None
            if(graph_node == None) :
                return False, next_task, current_Task

            if(graph_node.get_search_flag() == False and graph_node.check_prev() == -1) :
                graph_node.set_search_flag()
                current_Task = graph_node

            if(graph_node.check_prev() != -1) :
                next_task = graph_node.get_prev_node_as_dict()[graph_node.check_prev()]
            elif(graph_node.check_next() != -1):
                next_task = graph_node.get_next_node_as_dict()[graph_node.check_next()]

            return stop_flag, next_task, current_Task
        except Exception as e :
            raise Exception ("seach net node error")

    def _find_first_node(self, linked_list):
        """
        get first node from list
        :param linked_list:
        :return:
        """
        while(len(linked_list.get_prev_node()) > 0 ) :
            linked_list = linked_list.get_prev_node()[0]
        return linked_list


    def _get_all_nodes_list(self):
        """
        get execute class path
        :param node_id:
        :return:
        """
        # make query string (use raw query only when cate is too complicated)
        try:
            query_list = []
            query_list.append("SELECT ND.nn_wf_node_id, ND.wf_task_submenu_id_id, SB.wf_task_menu_id_id, ND.nn_wf_node_name   ")
            query_list.append("FROM  master_NN_WF_NODE_INFO ND JOIN master_WF_TASK_SUBMENU_RULE SB   ")
            query_list.append("      ON ND.wf_task_submenu_id_id =  SB.wf_task_submenu_id   ")
            query_list.append("WHERE ND.wf_state_id_id = %s")

            # parm_list : set parm value as list
            parm_list = []
            parm_list.append(str(self.nn_id) + "_" + str(self.wf_ver))

            with connection.cursor() as cursor:
                cursor.execute(''.join(query_list), parm_list)
                row = dictfetchall(cursor)
            return row
            #return row[0]['nn_wf_node_id'], row[0]['wf_task_submenu_id_id'], row[0]['wf_task_menu_id_id']
        except Exception as e:
            raise Exception(e)

    def _get_cached_class_pool(self, node_name_list):
        """

        :param node_name_list:
        :return:
        """
        try :
            class_list = {}
            for i in range(len(node_name_list)) :
                _path, _cls = self.get_cluster_exec_class(node_name_list[i]['nn_wf_node_id'])
                class_list[node_name_list[i]['nn_wf_node_id']] = self.load_class(_path, _cls)
            return class_list
        except Exception as e :
            raise Exception (e)

    def _get_node_rel_data(self):
        """
        get sequence of nodes to execute
        :return:
        """
        return_arr = []
        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=self.nn_id + "_" + self.wf_ver)
        for data in query_set:
            return_arr.append([data.nn_wf_node_id_1, data.nn_wf_node_id_2])
        return return_arr

    def _create_node_graph(self, node_list, class_list, node_rel_list):
        """
        get node graph
        :return:
        """
        try :
            # set inital node info
            for node in node_list :
                cls = class_list[node.get('nn_wf_node_id')]
                cls.set_node_name(node.get('nn_wf_node_id'))
                cls.set_node_type(node.get('wf_task_submenu_id_id'))
                cls.set_node_grp(node.get('wf_task_menu_id_id'))
                cls.set_node_def(node.get('nn_wf_unique_keynode_name'))
                cls.set_net_node_id(node.get('nn_wf_node_name'))
                cls.set_net_ver(self.wf_ver)
                cls.set_net_id(self.nn_id)

                for rel_node in node_rel_list :
                    if(node.get('nn_wf_node_id') == rel_node[0]) :
                        cls.set_next_node(rel_node[1], class_list[rel_node[1]])
                    if(node.get('nn_wf_node_id') == rel_node[1]):
                        cls.set_prev_node(rel_node[0], class_list[rel_node[0]])
                class_list[node.get('nn_wf_node_id')] = cls

            # set inital node info
            for node in reversed(node_list) :
                cls = class_list[node.get('nn_wf_node_id')]

                for rel_node in node_rel_list :
                    if(node.get('nn_wf_node_id') == rel_node[0]) :
                        cls.set_next_node(rel_node[1], class_list[rel_node[1]])
                    if(node.get('nn_wf_node_id') == rel_node[1]):
                        cls.set_prev_node(rel_node[0], class_list[rel_node[0]])
                class_list[node.get('nn_wf_node_id')] = cls

            return class_list[node_list[0].get('nn_wf_node_id')]
        except Exception as e :
            raise Exception (e)

