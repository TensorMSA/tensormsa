import importlib
from django.db import connection
from common.utils import *
from master import models
from konlpy.tag import Kkma
from konlpy.tag import Mecab
from konlpy.tag import Twitter
import warnings
from hanja import hangul
import numpy as np
import re
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
        self.net_id = ''
        self.net_ver = ''
        self.node_id = ''

    def run(self, conf_data):
        pass

    def _init_node_parm(self):
        pass

    def _set_progress_state(self):
        pass

    def set_net_node_id(self, node_id):
        """
        set flag for tree search
        :return:
        """
        self.node_id = node_id

    def get_net_node_id(self):
        """
        set flag for tree search
        :return:
        """
        return self.node_id

    def set_net_ver(self, net_ver):
        """
        set flag for tree search
        :return:
        """
        self.net_ver = net_ver

    def get_net_ver(self):
        """
        set flag for tree search
        :return:
        """
        return self.net_ver

    def set_net_id(self, net_id):
        """
        set flag for tree search
        :return:
        """
        self.net_id = net_id

    def get_net_id(self):
        """
        set flag for tree search
        :return:
        """
        return self.net_id

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

    def _mecab_parse(self, str_arr, tag_combine=True):
        """

        :param h5file:
        :return:
        """
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(mecab.pos(str(data)), tag_combine=tag_combine)
        return return_arr

    def _kkma_parse(self, str_arr, tag_combine=True):
        """

        :param h5file:
        :return:
        """
        kkma = Kkma()
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(kkma.pos(str(data)), tag_combine=tag_combine)
        return return_arr

    def _twitter_parse(self, str_arr, tag_combine=True):
        """

        :param h5file:
        :return:
        """
        twitter = Twitter(jvmpath=None)
        return_arr = []
        for data in str_arr:
            return_arr = return_arr + self._flat(twitter.pos(str(data)), tag_combine=tag_combine)
        return return_arr

    def _default_parse(self):
        pass

    def _flat(self, pos, tag_combine=True):
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
            if(tag_combine == True) :
                line_list.append("{0}/{1}".format(word, tag))
            else :
                line_list.append(word)

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
[pad_char] * pad_len + input
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

    def _find_netconf_node_id(self, nn_id, wf_ver = None):
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
        if wf_ver == None:
            query_list.append("     AND WV.ACTIVE_FLAG = 'Y'    ")
        else:
            query_list.append("     AND WV.NN_WF_VER_ID = "+str(wf_ver)+"    ")
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

    def _word_embed_data(self, embed_type, input_data, cls=None, embeder_id=None):
        """
        change word to vector
        :param input_data:
        :return:
        """
        return_arr = []
        if (cls) :
            embed_class = cls
        else :
            embed_class = self.onehot_encoder

        if (embeder_id) :
            w2v_id = embeder_id
        else :
            w2v_id = self.word_embed_id

        if(embed_type == 'onehot'):
            for data in input_data:
                row_arr = []
                for row in data :
                    row_arr = row_arr + embed_class.get_vector(row).tolist()
                return_arr.append(row_arr)
            return return_arr
        # elif (embed_type == 'w2v'):
        #     from cluster.service.service_predict_w2v import PredictNetW2V
        #     for data in input_data:
        #         parm = {"type": "train", "val_1": {}, "val_2": []}
        #         parm['val_1'] = data
        #         return_arr.append(PredictNetW2V().run(w2v_id, parm))
        #     return return_arr
        elif(embed_type == None) :
            return input_data
        else :
            raise Exception ("[Error] seq2seq train - word embeding : not defined type {0}".format(embed_type))

    def _pos_tag_predict_data(self, x_input, word_len):
        """

        :param x_input:
        :return:
        """
        word_list = []
        mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')
        for word_tuple in self._pad_predict_input(mecab.pos(x_input), word_len):
            if (len(word_tuple[1]) > 0):
                word = ''.join([word_tuple[0], "/", word_tuple[1]])
            else:
                word = word_tuple[0]
            word_list.append(word)
        return word_list

    def _pad_predict_input(self, input_tuple, word_len):
        """
        pad chars for prediction
        :param input_tuple:
        :return:
        """
        try :
            pad_size = word_len - (len(input_tuple) + 1)
            if(pad_size >= 0 ) :
                input_tuple = pad_size * [('#', '')] + input_tuple[0: word_len -1] + [('SF', '')]
            else :
                input_tuple = input_tuple[0: word_len-1] + [('SF', '')]
            return input_tuple
        except Exception as e:
            raise Exception(e)

    def _copy_node_parms(self, from_node, to_node):
        """
        copy node parm from a to b and save
        :param from_node:
        :param to_node:
        :return:
        """
        try :
            f_id = from_node.get_node_name()
            t_id = to_node.get_node_name()
            from_node_dict = from_node._get_node_parm(f_id)
            to_node_dict = to_node._get_node_parm(t_id)
            input_dict = {}
            for key in from_node_dict.get_view_obj(f_id).keys():
                if(key not in to_node_dict.get_view_obj(t_id).keys()) :
                    input_dict[key] = from_node_dict.get_view_obj(f_id)[key]
            to_node_dict.update_view_obj(t_id, input_dict)
        except Exception as e :
            raise Exception ("error on _copy_node_parms : {0}".format(e))

    def _get_node_parm(self):
        return self.wf_conf

    UNK = "$UNK$"
    NUM = "$NUM$"
    NONE = "O"

    def get_onehot_vector(self, sent):
        """
        convert sentecne to vector
        :return: list
        """
        try:
            return_vector = []
            embeddings = np.zeros([30])
            idx = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ']
            num_reg = re.compile("[0-9- ]")

            if (type(sent) not in [type('str'), type([])]):
                raise Exception("input must be str")

            if (type(sent) == type([])):
                sent = sent[0]

            for char in sent:
                vector_a = np.copy(embeddings)
                vector_b = np.copy(embeddings)
                vector_c = np.copy(embeddings)
                vector_d = np.copy(embeddings)

                if (num_reg.match(char) == None and hangul.is_hangul(char)):
                    anl = hangul.separate(char)
                    vector_a[anl[0] if anl[0] > 0 else 0] = 1
                    vector_b[anl[1] if anl[1] > 0 else 0] = 1
                    vector_c[anl[2] if anl[2] > 0 else 0] = 1
                elif (num_reg.match(char)):
                    vector_d[idx.index(char)] = 1
                return_vector.append(np.append(vector_a, [vector_b, vector_c, vector_d]))
            return np.array(return_vector)
        except Exception as e:
            print("error on get_onehot_vector : {0}".format(e))

    def get_onehot_word(self, vec_list):
        """
        convert sentecne to vector
        :return: list
        """
        idx = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ']
        return_vector = []
        if (len(vec_list) == 0 or len(vec_list[0]) != 120):
            raise Exception("input size error")

        for vec in vec_list:
            anl = np.array(vec).reshape(4, 30)

            if (np.argmax(anl[3]) > 0):
                return_vector.append(idx[np.argmax(anl) - 90])
            else:
                return_vector.append(hangul.build(np.argmax(anl[0]),
                                                  np.argmax(anl[1]),
                                                  np.argmax(anl[2])))
        return return_vector

    def write_char_embedding(self, vocab, trimmed_filename):
        """
        Writes a vocab to a file

        Args:
            vocab: iterable that yields word
            filename: path to vocab file
        Returns:
            write a word per line
        """
        try:
            print("Writing vocab...")
            embeddings = np.zeros([len(vocab), 120])
            if (type(vocab) == type(set())):
                vocab = list(vocab)
            for i, word in enumerate(vocab):
                embeddings[vocab.index(word)] = np.array(self.get_onehot_vector(word))[0]
            np.savetxt(trimmed_filename, embeddings)
            print("- done. {} tokens".format(len(vocab)))
        except Exception as e:
            print("error on write_char_embedding : {0}".format(e))

    def write_vocab(self, vocab, filename):
        """
        Writes a vocab to a file

        Args:
            vocab: iterable that yields word
            filename: path to vocab file
        Returns:
            write a word per line
        """
        print("Writing vocab...")
        with open(filename, "w+") as f:
            for i, word in enumerate(vocab):
                if i != len(vocab) - 1:
                    f.write("{}\n".format(word))
                else:
                    f.write(word)
        print("- done. {} tokens".format(len(vocab)))

    def get_vocabs(self, datasets, vocab=None, tags=None):
        """
        Args:
            datasets: a list of dataset objects
        Return:
            a set of all the words in the dataset
        """
        try:
            print("Building vocab...")
            if (vocab == None or tags == None):
                vocab_words = set()
                vocab_tags = set()
            else:
                vocab_words = set(vocab)
                vocab_tags = set(tags)

            for dataset in datasets:
                for words, tags in dataset:
                    vocab_words.update(words)
                    vocab_tags.update(tags)
            print("- done. {} tokens".format(len(vocab_words)))
            return vocab_words, vocab_tags
        except Exception as e:
            print("error on get_vacabs {0}".format(e))

    def load_vocab(self, filename):
        """
        Args:
            filename: file with a word per line
        Returns:
            d: dict[word] = index
        """
        d = dict()

        if(os.path.exists(filename) == False) :
            return d

        with open(filename) as f:
            for idx, word in enumerate(f):
                word = word.strip()
                d[word] = idx

        return d

    def export_trimmed_glove_vectors(self, vocab, model, trimmed_filename):
        """
        Saves glove vectors in numpy array

        Args:
            vocab: dictionary vocab[word] = index
            glove_filename: a path to a glove file
            trimmed_filename: a path where to store a matrix in npy
            dim: (int) dimension of embeddings
            UNK = "$UNK$"
            NUM = "$NUM$"
            NONE = "O"
        """
        try:
            embeddings = np.zeros([len(vocab), model.vector_size])
            for word in vocab:
                if (word != self.UNK):
                    embeddings[list(vocab).index(word)] = model[word]
            np.savetxt(trimmed_filename, embeddings)
        except Exception as e:
            print("error on export_trimmed_glove_vectors : {0}".format(e))

    def get_trimmed_glove_vectors(self, filename):
        """
        Args:
            filename: path to the npz file
        Returns:
            matrix of embeddings (np array)
        """
        with open(filename) as f:
            return np.loadtxt(f)

    def get_char_vocab(self, dataset, chars=None):
        """
        Args:
            dataset: a iterator yielding tuples (sentence, tags)
        Returns:
            a set of all the characters in the dataset
        """
        if (chars == None):
            vocab_char = set()
        else:
            vocab_char = set(chars)

        for words, _ in dataset:
            for word in words:
                vocab_char.update(word)

        return vocab_char

    def get_processing_word(self, vocab_words=None, vocab_chars=None,
                            lowercase=False, chars=False):
        """
        Args:
            vocab: dict[word] = idx
        Returns:
            f("cat") = ([12, 4, 32], 12345)
                     = (list of char ids, word id)
        """

        def f(word):
            # 0. get chars of words
            if vocab_chars is not None and chars == True:
                char_ids = []
                for char in word:
                    # ignore chars out of vocabulary
                    if char in vocab_chars:
                        char_ids += [vocab_chars[char]]

            # 1. preprocess word
            # if lowercase:
            #     word = word.lower()
            # if word.isdigit():
            #     word = NUM

            # 2. get id of word
            if vocab_words is not None:
                if word in vocab_words:
                    word = vocab_words[word]
                else:
                    word = vocab_words[self.UNK]

            # 3. return tuple char ids, word id
            if vocab_chars is not None and chars == True:
                return char_ids, word
            else:
                return word

        return f

    def minibatches(self, data, minibatch_size):
        """
        Args:
            data: generator of (sentence, tags) tuples
            minibatch_size: (int)
        Returns:
            list of tuples
        """
        x_batch, y_batch = [], []
        for (x, y) in data:
            if len(x_batch) == minibatch_size:
                yield x_batch, y_batch
                x_batch, y_batch = [], []

            if type(x[0]) == tuple:
                x = zip(*x)
            x_batch += [x]
            y_batch += [y]

        if len(x_batch) != 0:
            yield x_batch, y_batch

    def _pad_sequences(self, sequences, pad_tok, max_length):
        """
        Args:
            sequences: a generator of list or tuple
            pad_tok: the char to pad with
        Returns:
            a list of list where each sublist has same length
        """
        sequence_padded, sequence_length = [], []

        for seq in sequences:
            seq = list(seq)
            seq_ = seq[:max_length] + [pad_tok] * max(max_length - len(seq), 0)
            sequence_padded += [seq_]
            sequence_length += [min(len(seq), max_length)]

        return sequence_padded, sequence_length

    def get_chunks(self, seq, tags):
        """
        Args:
            seq: [4, 4, 0, 0, ...] sequence of labels
            tags: dict["O"] = 4
        Returns:
            list of (chunk_type, chunk_start, chunk_end)

        Example:
            seq = [4, 5, 0, 3]
            tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
            result = [("PER", 0, 2), ("LOC", 3, 4)]
        """
        try:
            default = tags[self.NONE]
            idx_to_tag = {idx: tag for tag, idx in iter(tags.items())}
            chunks = []
            chunk_type, chunk_start = None, None
            for i, tok in enumerate(seq):
                # End of a chunk 1
                if tok == default and chunk_type is not None:
                    # Add a chunk.
                    chunk = (chunk_type, chunk_start, i)
                    chunks.append(chunk)
                    chunk_type, chunk_start = None, None

                # End of a chunk + start of a chunk!
                elif tok != default:
                    tok_chunk_type = self.get_chunk_type(tok, idx_to_tag)
                    if chunk_type is None:
                        chunk_type, chunk_start = tok_chunk_type, i
                    # elif tok_chunk_type != chunk_type or tok[0] == "B":
                    elif tok_chunk_type != chunk_type:
                        chunk = (chunk_type, chunk_start, i)
                        chunks.append(chunk)
                        chunk_type, chunk_start = tok_chunk_type, i
                else:
                    pass
            # end condition
            if chunk_type is not None:
                chunk = (chunk_type, chunk_start, len(seq))
                chunks.append(chunk)
            return chunks
        except Exception as e:
            raise Exception(e)

    def pad_sequences(self, sequences, pad_tok, nlevels=1):
        """
        Args:
            sequences: a generator of list or tuple
            pad_tok: the char to pad with
        Returns:
            a list of list where each sublist has same length
        """
        if nlevels == 1:
            max_length = max(map(lambda x: len(x), sequences))
            sequence_padded, sequence_length = self._pad_sequences(sequences,
                                                                   pad_tok, max_length)

        elif nlevels == 2:
            max_length_word = max([max(map(lambda x: len(x), seq)) for seq in sequences])
            sequence_padded, sequence_length = [], []
            for seq in sequences:
                # all words are same length now
                sp, sl = self._pad_sequences(seq, pad_tok, max_length_word)
                sequence_padded += [sp]
                sequence_length += [sl]

            max_length_sentence = max(map(lambda x: len(x), sequences))
            sequence_padded, _ = self._pad_sequences(sequence_padded, [pad_tok] * max_length_word,
                                                     max_length_sentence)
            sequence_length, _ = self._pad_sequences(sequence_length, 0, max_length_sentence)

        return sequence_padded, sequence_length

    def get_chunk_type(self, tok, idx_to_tag):
        tag_name = idx_to_tag[tok]
        return tag_name.split('-')[-1]

    class CoNLLDataset(object):
        """
        Class that iterates over CoNLL Dataset
        """

        def __init__(self, filename, processing_word=None, processing_tag=None,
                     max_iter=None, all_line=True):
            """
            Args:
                filename: path to the file
                processing_words: (optional) function thsat takes a word as input
                processing_tags: (optional) function that takes a tag as input
                max_iter: (optional) max number of sentences to yield
            """
            self.filename = filename
            self.processing_word = processing_word
            self.processing_tag = processing_tag
            self.max_iter = max_iter
            self.length = None
            self.all_line = all_line

        def __iter__(self):
            try:
                niter = 0
                with open(self.filename) as f:
                    words, tags = [], []
                    for line in f:
                        line = line.strip()
                        if (len(line) == 0 or line.startswith("-DOCSTART-")):
                            if len(words) != 0:
                                niter += 1
                                if self.max_iter is not None and niter > self.max_iter:
                                    break
                                yield words, tags
                                words, tags = [], []
                        else:
                            word, tag = line.split(' ')
                            if self.processing_word is not None:
                                word = self.processing_word(word)
                            if self.processing_tag is not None:
                                tag = self.processing_tag(tag)
                            words += [word]
                            tags += [tag]

            except Exception as e:
                raise Exception(e)

        def __len__(self):
            """
            Iterates once over the corpus to set and store length
            """
            if self.length is None:
                self.length = 0
                for _ in self:
                    self.length += 1

            return self.length

    def _preprocess(self, input_data, type = None):
        """
        preprocess with language model
        :param input_data:
        :returnen:
        """
        if(type == None) :
            type = self.preprocess_type
        if(type == 'mecab') :
            return self._mecab_parse(input_data)
        elif (type == 'mecab_simple'):
            return self._mecab_parse(input_data, tag_combine=False)
        elif (type == 'kkma'):
            return self._kkma_parse(input_data)
        elif (type == 'twitter'):
            return self._twitter_parse(input_dadatata)
        else :
            return list(map(lambda x : x.split(' '), input_data))