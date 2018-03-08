from django.core import serializers as serial
from master import models
from master import serializers
from django.db import connection
from common.utils import dictfetchall
import json
from common.utils import *
import os
from master.automl.automl_rule import AutoMlRule
from master.workflow.common.workflow_state_menu import WorkFlowStateMenu

class WorkFlowSimpleManager :
    """

    """

    def __init__(self):
        self.netconf_node = ""
        self.netconf_data = ""
        self.netconf_data_conf = ""
        self.netconf_data_encode = ""
        self.netconf_data_decode = ""
        self.netconf_data_merge = ""
        self.netconf_feed = ""
        self.eval_node = ""
        self.eval_data = ""
        self.eval_feed = ""
        self.nn_id = ""
        self.nn_wf_ver_id = ""

    def set_node_name(self, net_node):
        graph_id = net_node[0]['fields']["graph_flow_info_id"]
        graph = WorkFlowStateMenu().get_graph_info(graph_id)
        for net in graph:
            if net['fields']['graph_node'] == 'netconf_node':
                self.netconf_node = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_data':
                self.netconf_data = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_data_conf':
                self.netconf_data_conf = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_data_encode':
                self.netconf_data_encode = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_data_decode':
                self.netconf_data_decode = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_data_merge':
                self.netconf_data_merge = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'netconf_feed':
                self.netconf_feed = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'eval_node':
                self.eval_node = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'eval_data':
                self.eval_data = net['fields']['graph_node_name']
            if net['fields']['graph_node'] == 'eval_feed':
                self.eval_feed = net['fields']['graph_node_name']

        self.group_id = net_node[0]['fields']["graph_flow_group_id"]

    def create_workflow(self, nn_id, wf_ver, type):
        """
        create workflow base node info
        :param nn_id:
        :return:
        """
        # crate state info with nn_id & workflow version
        input_data = {}
        input_data['nn_id'] = str(nn_id)
        input_data['nn_wf_ver_id'] = str(wf_ver)
        input_data['wf_state_id'] = str(nn_id) + "_" + str(wf_ver)
        self.nn_id = str(nn_id)
        self.nn_wf_ver_id = str(wf_ver)
        state_id = self._create_workflow_state(input_data)

        #todo 나중에 꼭 지울것!!!!!!!! 임시방편 it is temporary solution
        if (type =='frame'):
            type = 'wdnn'

        # create nodes fit to requested type (img, text, frame)
        net_node = AutoMlRule().get_graph_info(type, "all")
        self.set_node_name(net_node)

        if(type == 'cnn'):
            self._create_predefined_nodes_cnn(state_id)
        # elif(type == 'resnet'):
        #     self._create_predefined_nodes_renet(state_id)
        elif(type == 'frame' or type == "wdnn" or type == "dnn" or type =="wdnn_reg"):
            self._create_predefined_nodes_wdnn(state_id)
        elif (type == 'ml'):
            self._create_predefined_nodes_ml(state_id)
        elif(type == 'keras_frame' or type == "wdnn_keras"):
            self._create_predefined_nodes_keras_frame(state_id)
        elif(type == 'word2vec'):
            self._create_predefined_nodes_word2vec(state_id)
        elif(type == 'word2vec_frame'):
            self._create_predefined_nodes_word2vec_frame(state_id)
        elif(type == 'doc2vec'):
            self._create_predefined_nodes_doc2vec(state_id)
        elif(type == 'wcnn'):
            self._create_predefined_nodes_wcnn_frame(state_id)
        elif(type == 'seq2seq'):
            self._create_predefined_nodes_seq2seq(state_id)
        elif(type == 'seq2seq_csv') :
            self._create_predefined_nodes_seq2seq_csv(state_id)
        elif(type == 'autoencoder_img'):
            self._create_predefined_nodes_autoencoder_img(state_id)
        elif(type == 'autoencoder_csv'):
            self._create_predefined_nodes_autoencoder_csv(state_id)
        elif(type == 'bilstmcrf_iob') :
            self._create_predefined_nodes_bilstmcrf_iob(state_id)
        elif(type == 'fasttext_txt'):
            self._create_predefined_nodes_fasttext_txt(state_id)
        elif(type == 'ngram_mro'):
            self._create_predefined_nodes_frame(state_id)
        elif(type == 'xgboost_reg'):
            self._create_predefined_nodes_xgboost(state_id)
        else :
            if self.group_id == '1': #Frame
                self._create_predefined_nodes_frame(state_id)
            elif self.group_id == '2': #Image
                self._create_predefined_nodes_image(state_id)
            elif self.group_id == '3': #NLP
                self._create_predefined_nodes_nlp(state_id)
            else:
                raise Exception ("Error : Not defined type ("+type+")")

        return type

    def _create_workflow_state(self, input_data):
        """

        :return:
        """
        try:
            serializer = serializers.NN_WF_STATE_INFO_Serializer(data=input_data)
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            raise Exception(e)
        finally:
            return input_data['wf_state_id']

    def __put_nn_wf_node_relation(self, input_data):
        """

        :param input_data:
        :return:
        """
        try:
            serializer = serializers.NN_WF_NODE_RELATION_Serializer(data=input_data)
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            print(e)
            raise Exception(e)
        finally:
            return input_data['wf_state_id']

    def __put_nn_wf_node_info(self, input_data):
        """

        :param input_data:
        :return:
        """
        try:
            serializer = serializers.NN_WF_NODE_INFO_Serializer(data=input_data)
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            print(e)
            raise Exception(e)
        finally:
            return input_data['wf_state_id']

    def _set_nn_wf_node_info(self, wf_state_id, node, submenu_id):
        input_data = {}
        input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + node
        input_data['nn_wf_node_name'] = node
        input_data['wf_state_id'] = str(wf_state_id)
        input_data['wf_task_submenu_id'] = submenu_id
        input_data['wf_node_status'] = 0
        input_data['node_config_data'] = {}
        input_data['node_draw_x'] = 0
        input_data['node_draw_y'] = 0
        input_data['nn_id'] = str(self.nn_id)
        input_data['nn_wf_ver_id'] = str(self.nn_wf_ver_id)
        self.__put_nn_wf_node_info(input_data)

    def _set_nn_wf_node_relation(self, wf_state_id, node1, node2):
        input_data = {}
        input_data['wf_state_id'] = str(wf_state_id)
        input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + node1
        input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + node2
        self.__put_nn_wf_node_relation(input_data)

    def _create_predefined_nodes_frame(self, wf_state_id):
        """
        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_conf, 'data_dfconf')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'nf_frame')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_data_conf)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_conf, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_image(self, wf_state_id):
        """
        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info(wf_state_id, self.netconf_data, 'data_image')
            self._set_nn_wf_node_info(wf_state_id, self.netconf_feed, 'pre_feed_image')
            self._set_nn_wf_node_info(wf_state_id, self.netconf_node, 'nf_image')

            # eval info
            self._set_nn_wf_node_info(wf_state_id, self.eval_data, 'data_image')
            self._set_nn_wf_node_info(wf_state_id, self.eval_feed, 'pre_feed_image')
            self._set_nn_wf_node_info(wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.netconf_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_nlp(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_nlp')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'nf_nlp')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_nlp')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_cnn(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_image')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_img2cnn')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'nf_cnn')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_image')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_img2cnn')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.netconf_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_renet(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info(wf_state_id, self.netconf_data, 'data_image')
            self._set_nn_wf_node_info(wf_state_id, self.netconf_feed, 'pre_feed_img2renet')
            self._set_nn_wf_node_info(wf_state_id, self.netconf_node, 'nf_renet')

            # eval info
            self._set_nn_wf_node_info(wf_state_id, self.eval_data, 'data_image')
            self._set_nn_wf_node_info(wf_state_id, self.eval_feed, 'pre_feed_img2renet')
            self._set_nn_wf_node_info(wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.netconf_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_wdnn(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_conf, 'data_dfconf')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2wdnn')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'nf_wdnn')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_fr2wdnn')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_data_conf)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_conf, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True
    def _create_predefined_nodes_xgboost(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info pre_feed_fr2wdnn
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            #self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2xg')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'nf_xgboost')
            #self._set_nn_wf_node_info(wf_state_id, self.eval_data, 'data_frame')
            #self._set_nn_wf_node_info(wf_state_id, self.eval_node, 'eval_normal')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_node)
            #self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            #self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            #self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_data)
            #self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_node)


        except Exception as e:
            raise Exception(e)
        finally:
            return True


    def _create_predefined_nodes_ml(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_conf, 'data_dfconf')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2ml')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'nf_ml')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_fr2ml')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_data_conf)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_conf, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.netconf_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_keras_frame(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_conf, 'data_dfconf')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_keras2frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'keras_dnn')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_keras2frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_data_conf)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_conf, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_word2vec(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_text')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_text2wv')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'word_to_vec')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_text')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_text2wv')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_word2vec_frame(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2wv_train')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'word_to_vec')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_fr2wv_test')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_doc2vec(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_raw')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_text2dv')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'doc_to_vec')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_raw')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_text2dv')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_wcnn_frame(self, wf_state_id):
        """
        wide and cnn with frame data init graph flow
        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2wcnn')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'wcnn')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_fr2wcnn')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_seq2seq(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_encode, 'data_text')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_decode, 'data_text')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data_merge, 'pre_merge')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_text2seq')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'seq_to_seq')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_text2seq')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_encode, self.netconf_data_merge)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_decode, self.netconf_data_merge)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_merge, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data_merge, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_feed)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_seq2seq_csv(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2seq')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'seq_to_seq')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_fr2seq')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_autoencoder_img(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_image')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_img2auto')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'autoencoder')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_autoencoder_csv(self, wf_state_id):
        """

        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_fr2auto')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'autoencoder')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_frame')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_fr2auto')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_bilstmcrf_iob(self, wf_state_id):
        """
        wide and cnn with frame data init graph flow
        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_iob')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_iob2bilstmcrf')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'bilstmcrf')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_iob')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_iob2bilstmcrf')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True


    def _create_predefined_nodes_fasttext_txt(self, wf_state_id):
        """
        wide and cnn with frame data init graph flow
        :return:
        """
        try:
            # netconf info
            self._set_nn_wf_node_info( wf_state_id, self.netconf_data, 'data_text')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_feed, 'pre_feed_text2fasttext')
            self._set_nn_wf_node_info( wf_state_id, self.netconf_node, 'fasttext')

            # eval info
            self._set_nn_wf_node_info( wf_state_id, self.eval_data, 'data_text')
            self._set_nn_wf_node_info( wf_state_id, self.eval_feed, 'pre_feed_iob2bilstmcrf')
            self._set_nn_wf_node_info( wf_state_id, self.eval_node, 'eval_extra')

            # netconf relation
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_data, self.netconf_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_feed, self.netconf_node)
            self._set_nn_wf_node_relation(wf_state_id, self.netconf_node, self.eval_node)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_data, self.eval_feed)
            self._set_nn_wf_node_relation(wf_state_id, self.eval_feed, self.eval_node)

        except Exception as e:
            raise Exception(e)
        finally:
            return True