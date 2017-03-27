import importlib
from django.db import connection
from common.utils import *
from master import models
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
from common import utils
import os,h5py

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
        try:
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
        except Exception as e:
            raise Exception(e)


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
        prev_grp = []
        prev_type = []
        next_arr = []
        next_grp = []
        next_type = []

        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=nn_id + "_" + wf_ver)

        for data in query_set:
            if(node_id == data.nn_wf_node_id_2) :
                prev_arr.append(data.nn_wf_node_id_1)
                submenu1 = models.NN_WF_NODE_INFO.objects.filter(nn_wf_node_id=data.nn_wf_node_id_1)[0].wf_task_submenu_id_id
                menu1 = models.WF_TASK_SUBMENU_RULE.objects.filter(wf_task_submenu_id=submenu1)[0].wf_task_menu_id_id
                prev_type.append(submenu1)
                prev_grp.append(menu1)
            if (node_id == data.nn_wf_node_id_1):
                next_arr.append(data.nn_wf_node_id_2)
                submenu2 = models.NN_WF_NODE_INFO.objects.filter(nn_wf_node_id=data.nn_wf_node_id_2)[0].wf_task_submenu_id_id
                menu2 = models.WF_TASK_SUBMENU_RULE.objects.filter(wf_task_submenu_id=submenu2)[0].wf_task_menu_id_id
                next_type.append(submenu2)
                next_grp.append(menu2)

        return_obj['prev'] = prev_arr
        return_obj['prev_grp'] = prev_grp
        return_obj['prev_type'] = prev_type
        return_obj['next'] = next_arr
        return_obj['next_grp'] = next_grp
        return_obj['next_type'] = next_type

        return return_obj

    def _get_forward_node_with_type(self, node_id, type):
        """
        get node relations connected with selected node_id
        :return:
        """
        try :
            return_list = []
            node_list = []
            node_list.append(node_id)

            while(len(node_list) > 0) :
                # make query string (use raw query only when cate is too complicated)
                query_list = []
                query_list.append("SELECT NI.NN_WF_NODE_ID, SR.WF_TASK_MENU_ID_ID  ")
                query_list.append("FROM MASTER_NN_WF_NODE_RELATION WR JOIN MASTER_NN_WF_NODE_INFO NI    ")
                query_list.append("     ON WR.NN_WF_NODE_ID_2 = NI.NN_WF_NODE_ID    ")
                query_list.append("     AND WR.NN_WF_NODE_ID_1 = %s    ")
                query_list.append("     JOIN MASTER_WF_TASK_SUBMENU_RULE SR  ")
                query_list.append("     ON SR.WF_TASK_SUBMENU_ID = NI.WF_TASK_SUBMENU_ID_ID    ")

                # parm_list : set parm value as list
                parm_list = []
                parm_list.append(node_list[0])

                with connection.cursor() as cursor:
                    cursor.execute(''.join(query_list), parm_list)
                    row = dictfetchall(cursor)
                    del node_list[0]

                for i in range(len(row)) :
                    node_list.append(row[i]['nn_wf_node_id'])
                    if (row[i]['wf_task_menu_id_id'] == type):
                        return_list.append(row[i]['nn_wf_node_id'])


            return return_list
        except Exception as e :
            raise Exception (e)

    def _get_backward_node_with_type(self, node_id, type):
        """
        get node relations connected with selected node_id
        :return:
        """
        try:
            return_list = []
            node_list = []
            node_list.append(node_id)

            while (len(node_list) > 0):
                # make query string (use raw query only when cate is too complicated)
                query_list = []
                query_list.append("SELECT NI.NN_WF_NODE_ID, SR.WF_TASK_MENU_ID_ID  ")
                query_list.append("FROM MASTER_NN_WF_NODE_RELATION WR JOIN MASTER_NN_WF_NODE_INFO NI    ")
                query_list.append("     ON WR.NN_WF_NODE_ID_1 = NI.NN_WF_NODE_ID    ")
                query_list.append("     AND WR.NN_WF_NODE_ID_2 = %s    ")
                query_list.append("     JOIN MASTER_WF_TASK_SUBMENU_RULE SR  ")
                query_list.append("     ON SR.WF_TASK_SUBMENU_ID = NI.WF_TASK_SUBMENU_ID_ID    ")

                # parm_list : set parm value as list
                parm_list = []
                parm_list.append(node_list[0])

                with connection.cursor() as cursor:
                    cursor.execute(''.join(query_list), parm_list)
                    row = dictfetchall(cursor)
                    del node_list[0]

                for i in range(len(row)):
                    node_list.append(row[i]['nn_wf_node_id'])
                    if (row[i]['wf_task_menu_id_id'] == type):
                        return_list.append(row[i]['nn_wf_node_id'])

            return return_list
        except Exception as e:
            raise Exception(e)

    def _mecab_parse(self, str_arr):
        """

        :param h5file:
        :return:
        """
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(mecab.pos(data))
        return return_arr

    def _kkma_parse(self, str_arr):
        """

        :param h5file:
        :return:
        """
        kkma = Kkma()
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(kkma.pos(data))
        return return_arr

    def _twitter_parse(self, str_arr):
        """

        :param h5file:
        :return:
        """
        twitter = Twitter(jvmpath=None)
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(twitter.pos(data))
        return return_arr

    def _default_parse(self):
        pass

    def _flat(self, pos):
        """
        flat corpus for gensim
        :param pos:
        :return:
        """
        doc_list = []
        line_list = []
        count = 0
        for word, tag in pos :
            count = count + 1
            line_list.append("{0}/{1}".format(word, tag))
            #Add POS Tagging for divide (kkma and twitter)
            if(tag == 'SF' or tag == 'Punctuation' or len(pos) == count) :
                if(len(line_list) > self.sent_max_len - 1) :
                    line_list = line_list[0:self.sent_max_len-1]
                else :
                    pad_len = (self.sent_max_len - (len(line_list)+1))
                    line_list = line_list + ['#'] * pad_len
                line_list.append('SF')
                doc_list.append(line_list)
                line_list = []
        return doc_list