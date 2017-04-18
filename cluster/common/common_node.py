import importlib
from django.db import connection
from common.utils import *
from master import models
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
import warnings
import os,h5py

class WorkFlowCommonNode :
    """
        wdnn을 위한 load data를 위한 빈 메소드 생성
    """
    def __init__(self):
        self.prev_nodes = {}
        self.next_nodes = {}
        self.node_name = ''
        self.node_grp = ''
        self.node_type = ''
        self.node_def = ''
        self.search_flag = False

    def run(self, conf_data):
        pass

    def _init_node_parm(self):
        pass

    def _set_progress_state(self):
        pass

    def set_search_flag(self):
        """
        set flag for tree search
        :return:
        """
        self.search_flag = True

    def get_search_flag(self):
        """
        set flag for tree search
        :return:
        """
        return self.search_flag

    def set_next_node(self, key, node_cls):
        """
        next node class
        :param name:
        :return:
        """
        self.next_nodes[key] = node_cls

    def check_next(self):
        """
        check if next nodes are all searched
        :param name:
        :return:
        """
        for node in self.next_nodes.keys() :
            if(self.next_nodes[node].get_search_flag() == False) :
                return node
        return -1

    def check_prev(self):
        """
        check if prev nodes are all searched
        :param name:
        :return:
        """
        for node in self.prev_nodes.keys() :
            if(self.prev_nodes[node].get_search_flag() == False) :
                return node
        return -1

    def get_next_node(self, grp=None, type=None):
        """
        next node class
        :param name:
        :return:
        """
        return_list = []
        for name in self.next_nodes.keys() :
            if ((grp == None or grp == self.next_nodes[name].get_node_grp()) and
                    (type == None or type == self.next_nodes[name].get_node_type())):
                return_list.append(self.next_nodes[name])
        return return_list

    def get_next_node_as_dict(self):
        """
        next node class
        :param name:
        :return:
        """
        return self.next_nodes

    def set_prev_node(self, key, node_cls):
        """
        prev_node class
        :param name:
        :return:
        """
        self.prev_nodes[key] = node_cls

    def get_prev_node(self, grp=None, type=None):
        """
        prev_node class
        :param name:
        :return:
        """
        return_list = []
        for name in self.prev_nodes.keys() :
            if ((grp == None or grp == self.prev_nodes[name].get_node_grp()) and
                    (type == None or type == self.prev_nodes[name].get_node_type())):
                return_list.append(self.prev_nodes[name])
        return return_list

    def get_prev_node_as_dict(self):
        """
        prev_node class
        :param name:
        :return:
        """
        return self.prev_nodes

    def set_node_name(self, node_name):
        """
        node name string
        :param name:
        :return:
        """
        self.node_name = node_name

    def get_node_name(self):
        """
        node name string
        :param name:
        :return:
        """
        return self.node_name

    def get_node_def(self):
        """
        node name string
        :param name:
        :return:
        """
        return self.node_def

    def set_node_def(self, name):
        """
        node name string
        :param name:
        :return:
        """
        self.node_def = name

    def set_node_grp(self, node_grp):
        """
        node name string
        :param name:
        :return:
        """
        self.node_grp = node_grp

    def get_node_grp(self):
        """
        node name string
        :param name:
        :return:
        """
        return self.node_grp

    def set_node_type(self, node_type):
        """
        node name string
        :param name:
        :return:
        """
        self.node_type = node_type

    def get_node_type(self):
        """
        node name string
        :param name:
        :return:
        """
        return self.node_type

    def get_linked_next_node_with_grp(self, grp):
        """
        get linked node forward with type
        :param type:
        :return:
        """
        return_obj_list = []
        obj = self

        obj_next = obj.get_next_node()
        if(len(obj_next) == 0):
            return []

        for i in range(len(obj_next)):
            if(obj_next[i].get_node_grp() == grp) :
                return_obj_list.append(obj_next[i])
            return  return_obj_list + obj_next[i].get_linked_next_node_with_grp(grp)

    def get_linked_prev_node_with_cond(self, val, cond='has_value'):
        """
        get linked node prev until find node which have specific parm
        :param type:
        :return:
        """
        return_obj_list = []
        obj = self

        obj_prev = obj.get_prev_node()
        if(len(obj_prev) == 0):
            return []

        for i in range(len(obj_prev)):
            if(val in obj_prev[i].__dict__) :
                return_obj_list.append(obj_prev[i])
            return  return_obj_list + obj_prev[i].get_linked_prev_node_with_grp(val)

    def get_linked_prev_node_with_grp(self, grp):
        """
        get linked node prev with type
        :param type:
        :return:
        """
        return_obj_list = []
        obj = self

        obj_prev = obj.get_prev_node()
        if(len(obj_prev) == 0):
            return []

        for i in range(len(obj_prev)):
            if(obj_prev[i].get_node_grp() == grp) :
                return_obj_list.append(obj_prev[i])
            return  return_obj_list + obj_prev[i].get_linked_prev_node_with_grp(grp)

    def get_linked_prev_node_with_type(self, type):
        """
        get linked node forward with type
        :param type:
        :return:
        """
        return_obj_list = []
        obj = self

        obj_prev = obj.get_prev_node()
        if(len(obj_prev) == 0):
            return []

        for i in range(len(obj_prev)):
            if(obj_prev[i].get_node_type() == type) :
                return_obj_list.append(obj_prev[i])
            return  return_obj_list + obj_prev[i].get_linked_prev_node_with_type(type)

    def get_linked_next_node_with_type(self, type):
        """
        get linked node forward with type
        bug fix prev node to next node
        :param type:
        :return:
        """
        return_obj_list = []
        obj = self

        obj_next = obj.get_next_node()
        if(len(obj_next) == 0):
            return []

        for i in range(len(obj_next)):
            if(obj_next[i].get_node_type() == type) :
                return_obj_list.append(obj_next[i])
            return  return_obj_list + obj_next[i].get_linked_next_node_with_type(type)

    def find_prev_node(self, node_name, node_list):
        """
        find prev node and return name
        :param node_name:
        :param node_list:
        :return:
        """
        #TODO : will be deprecated
        warnings.warn("find_prev_node will be deprecated !! ")
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
        # TODO : will be deprecated
        warnings.warn("find_next_node will be deprecated !! ")
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
        # TODO : will be deprecated
        warnings.warn("_get_node_relation will be deprecated !! ")
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
        # TODO : will be deprecated
        warnings.warn("_get_forward_node_with_type will be deprecated !! ")
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
        # TODO : will be deprecated
        warnings.warn("_get_backward_node_with_type will be deprecated !! ")
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
            return_arr = return_arr + self._flat(mecab.pos(str(data)))
        return return_arr

    def _kkma_parse(self, str_arr):
        """

        :param h5file:
        :return:
        """
        kkma = Kkma()
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(kkma.pos(str(data)))
        return return_arr

    def _twitter_parse(self, str_arr):
        """

        :param h5file:
        :return:
        """
        twitter = Twitter(jvmpath=None)
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(twitter.pos(str(data)))
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
        max_len = len(pos)
        for word, tag in pos :
            count = count + 1
            line_list.append("{0}/{1}".format(word, tag))
            #Add POS Tagging for divide (kkma and twitter)
            if(tag in ['Punctuation','SF']) :
                line_list.append('SF')
                doc_list.append(line_list)
                line_list = []
            elif(count >= max_len) :
                line_list.append('SF')
                doc_list.append(line_list)
                line_list = []
        return doc_list

    def encode_pad(self, input_list, max_len = 0, pad_char = '#'):
        """

        :param pos:
        :return:
        """
        output_list = []
        if(max_len == 0) :
            max_len = self.sent_max_len

        for input in input_list :
            if (len(input) > max_len):
                output_list.append(input[0:max_len])
            else:
                pad_len = (max_len - len(input))
                output_list.append([pad_char] * pad_len + input)
        return output_list

    def decode_pad(self, input_list, max_len = 0, pad_char = '#', start_char = '@'):
        """

        :param pos:
        :return:
        """
        output_list = []
        if(max_len == 0) :
            max_len = self.sent_max_len

        for input in input_list :
            if (len(input) > max_len - 1):
                output_list.append([start_char] + input[0:max_len-1])
            else:
                pad_len = (max_len - (len(input) + 1))
                output_list.append([start_char] + input + [pad_char] * pad_len)
        return output_list

    def load_data(self, node_id, parm = 'all'):
        pass

    def _find_netconf_node_id(self, nn_id):
        """
        return node id of netconf
        :param nn_id:
        :param version:
        :return:
        """

        # make query string (use raw query only when cate is too complicated)
        query_list = []
        query_list.append("SELECT NI.NN_WF_NODE_ID  ")
        query_list.append("FROM MASTER_NN_VER_WFLIST_INFO WV JOIN MASTER_NN_WF_STATE_INFO WS   ")
        query_list.append("     ON WV.NN_WF_VER_ID =  WS.NN_WF_VER_ID_ID    ")
        query_list.append("     AND WV.NN_ID_ID = WS.NN_ID    ")
        query_list.append("     AND WV.ACTIVE_FLAG = 'Y'    ")
        query_list.append("     AND WV.NN_ID_ID = %s    ")
        query_list.append("     JOIN MASTER_NN_WF_NODE_INFO NI    ")
        query_list.append("     ON WS.WF_STATE_ID = NI.WF_STATE_ID_ID    ")
        query_list.append("     JOIN MASTER_WF_TASK_SUBMENU_RULE SR  ")
        query_list.append("     ON SR.WF_TASK_SUBMENU_ID = NI.WF_TASK_SUBMENU_ID_ID    ")
        query_list.append("     AND SR.WF_TASK_MENU_ID_ID = 'netconf'")

        # parm_list : set parm value as list
        parm_list = []
        parm_list.append(nn_id)

        with connection.cursor() as cursor:
            cursor.execute(''.join(query_list), parm_list)
            row = dictfetchall(cursor)
        if(len(row) > 0):
            return row[0]['nn_wf_node_id']
        else :
            raise Exception ("No Active version Exist for predict service !")