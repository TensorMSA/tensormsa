from django.core import serializers as serial
from master import models
from master import serializers
from django.db import connection
from common.utils import dictfetchall
import json
from common.utils import *
import os

class WorkFlowSimpleManager :
    """

    """

    def __init__(self):
        self.train_node = "netconf_node"
        self.train_data_node = "datasrc"
        self.train_feed_node = "data_src_feeder"
        self.eval_node = "eval_node"
        self.eval_data_node = "evaldata"
        self.eval_feed_node = "data_eval_feeder"

        self.train_data = "train_data"
        self.eval_data = "eval_data"
        self.feed_train_data = "feed_train_data"
        self.feed_eval_data = "feed_eval_data"

    def get_train_node(self):
        return self.train_node

    def get_train_data_node(self):
        return self.train_data_node

    def get_train_feed_node(self):
        return self.train_feed_node

    def get_eval_node(self):
        return self.eval_node

    def get_eval_data_node(self):
        return self.eval_data_node

    def get_eval_feed_node(self):
        return self.eval_feed_node

    def _create_path_folder(self, nn_id, wf_ver):
        model_path = get_model_path(nn_id, wf_ver, self.train_node)
        train_source_path = get_source_path(nn_id, wf_ver, self.train_data_node)
        train_store_path = get_store_path(nn_id, wf_ver, self.train_data_node)
        eval_source_path = get_source_path(nn_id, wf_ver, self.eval_data_node)
        eval_store_path = get_store_path(nn_id, wf_ver, self.eval_data_node)

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
        state_id = self._create_workflow_state(input_data)

        # create nodes fit to requested type (img, text, frame)
        if(type == 'cnn'):
            self._create_predefined_nodes_cnn(state_id)
            self._create_path_folder(nn_id, wf_ver)
        elif(type == 'resnet'):
            self._create_predefined_nodes_renet(state_id)
        elif(type == 'word2vec'):
            self._create_predefined_nodes_word2vec(state_id)
        elif(type == 'doc2vec'):
            self._create_predefined_nodes_doc2vec(state_id)
        elif(type == 'frame' or type == "wdnn"):
            self._create_predefined_nodes_frame(state_id)
        elif(type == 'seq2seq'):
            self._create_predefined_nodes_seq2seq(state_id)
        elif(type == 'seq2seq_csv') :
            self._create_predefined_nodes_seq2seq_csv(state_id)
        elif(type == 'autoencoder_img'):
            self._create_predefined_nodes_autoencoder_img(state_id)
        elif(type == 'autoencoder_csv'):
            self._create_predefined_nodes_autoencoder_csv(state_id)
        elif(type == 'word2vec_frame'):
            self._create_predefined_nodes_word2vec_frame(state_id)
        elif(type == 'wcnn'):
            self._create_predefined_nodes_wcnn_frame(state_id)
        elif(type == 'keras_frame'):
            self._create_predefined_nodes_keras_frame(state_id)
        elif(type == 'bilstmcrf_iob') :
            self._create_predefined_nodes_bilstmcrf_iob(state_id)
        elif (type == 'fasttext_txt'):
            self._create_predefined_nodes_fasttext_txt(state_id)
        else :
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

    def _create_predefined_nodes_cnn(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.train_data_node
            input_data['nn_wf_node_name'] = self.train_data_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_image'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.train_feed_node
            input_data['nn_wf_node_name'] = self.train_feed_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_img2cnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.train_node
            input_data['nn_wf_node_name'] = self.train_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'nf_cnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.eval_data_node
            input_data['nn_wf_node_name'] = self.eval_data_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_image'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.eval_feed_node
            input_data['nn_wf_node_name'] = self.eval_feed_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_img2cnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.eval_node
            input_data['nn_wf_node_name'] = self.eval_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.train_data_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.train_feed_node
            self.__put_nn_wf_node_relation(input_data)

            nput_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.train_feed_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.train_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.train_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.eval_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.eval_data_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.eval_feed_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.eval_feed_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.eval_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.eval_feed_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.train_node
            self.__put_nn_wf_node_relation(input_data)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_renet(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.train_data_node
            input_data['nn_wf_node_name'] = self.train_data_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_image'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.train_node
            input_data['nn_wf_node_name'] = self.train_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'nf_renet'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.train_feed_node
            input_data['nn_wf_node_name'] = self.train_feed_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_img2renet'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.eval_data_node
            input_data['nn_wf_node_name'] = self.eval_data_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_image'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.eval_feed_node
            input_data['nn_wf_node_name'] = self.eval_feed_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_img2renet'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_' + self.eval_node
            input_data['nn_wf_node_name'] = self.eval_node
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.train_data_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.train_feed_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.train_feed_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.train_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.eval_data_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.eval_feed_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.eval_feed_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.train_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.train_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.eval_node
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_' + self.eval_feed_node
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_' + self.eval_node
            self.__put_nn_wf_node_relation(input_data)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_word2vec(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_name'] = 'test_data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'word_to_vec'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_text2wv_test'
            input_data['nn_wf_node_name'] = '_pre_feed_text2wv_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2wv'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_text2wv_train'
            input_data['nn_wf_node_name'] = 'pre_feed_text2wv'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2wv'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_text2wv_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_text2wv_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_text2wv_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_text2wv_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
        except Exception as e:
            raise Exception(e)
        finally:
            return True


    def _create_predefined_nodes_doc2vec(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_raw'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_name'] = 'test_data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_raw'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'doc_to_vec'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_text2dv_test'
            input_data['nn_wf_node_name'] = '_pre_feed_text2dv_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2dv'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_text2dv_train'
            input_data['nn_wf_node_name'] = 'pre_feed_text2dv'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2dv'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_text2dv_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_text2dv_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_text2dv_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_text2dv_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_frame(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_dataconf_node'
            input_data['nn_wf_node_name'] = 'dataconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_dfconf'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed data node   "nn00002_1_pre_feed_text2wv_train"
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_fr2wdnn_train'
            input_data['nn_wf_node_name'] = 'pre_feed_fr2wdnn_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2wdnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)


            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'nf_wdnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_name'] = 'evaldata'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed data node   "nn00002_1_pre_feed_text2wv_train"
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_fr2wdnn_test'
            input_data['nn_wf_node_name'] = 'pre_feed_fr2wdnn_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2wdnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # eval node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)




            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_dataconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_dataconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_fr2wdnn_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_fr2wdnn_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_fr2wdnn_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_fr2wdnn_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_keras_frame(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_dataconf_node'
            input_data['nn_wf_node_name'] = 'dataconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_dfconf'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed data node   "nn00002_1_pre_feed_text2wv_train"
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_keras2frame_train'
            input_data['nn_wf_node_name'] = 'pre_feed_keras2frame_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_keras2frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)


            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'keras_dnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_name'] = 'evaldata'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed data node   "nn00002_1_pre_feed_text2wv_train"
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_keras2frame_test'
            input_data['nn_wf_node_name'] = 'pre_feed_keras2frame_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_keras2frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # eval node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)




            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_dataconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_dataconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_keras2frame_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_keras2frame_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_keras2frame_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_keras2frame_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_seq2seq(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_encode_node'
            input_data['nn_wf_node_name'] = 'data_encode_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_decode_node'
            input_data['nn_wf_node_name'] = 'data_decode_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # preprocess merge node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_text_merge_node'
            input_data['nn_wf_node_name'] = 'text_merge_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_merge'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_text2seq_train'
            input_data['nn_wf_node_name'] = '_feed_text2seq_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2seq'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'seq_to_seq'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_text2seq_test'
            input_data['nn_wf_node_name'] = '_feed_text2seq_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2seq'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_encode_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_text_merge_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_decode_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_text_merge_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_text_merge_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_text2seq_train'
            self.__put_nn_wf_node_relation(input_data)


            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_text2seq_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_text_merge_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_text2seq_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_text2seq_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_seq2seq_csv(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_csv_node'
            input_data['nn_wf_node_name'] = 'data_csv_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_fr2seq'
            input_data['nn_wf_node_name'] = 'feed_fr2seq'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2seq'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'seq_to_seq'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_name'] = 'evaldata'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_fr2seq_test'
            input_data['nn_wf_node_name'] = 'feed_fr2seq_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2seq'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_csv_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_fr2seq'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_fr2seq'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_fr2seq_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_fr2seq_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_autoencoder_img(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_name'] = 'datasrc'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_image'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_img2auto_train'
            input_data['nn_wf_node_name'] = 'feed_img2auto_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_img2auto'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'autoencoder'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)



            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_img2auto_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_img2auto_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_autoencoder_csv(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_name'] = 'datasrc'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_train'
            input_data['nn_wf_node_name'] = 'feed_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2auto'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'autoencoder'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_name'] = 'evaldata'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_feed_test'
            input_data['nn_wf_node_name'] = 'feed_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2auto'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_evaldata'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_feed_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_feed_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

        except Exception as e:
            raise Exception(e)
        finally:
            return True

    def _create_predefined_nodes_word2vec_frame(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_name'] = 'test_data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'word_to_vec'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_fr2wv_test'
            input_data['nn_wf_node_name'] = 'pre_feed_fr2wv_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2wv'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_fr2wv_train'
            input_data['nn_wf_node_name'] = 'pre_feed_fr2wv_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2wv'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_fr2wv_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_fr2wv_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_fr2wv_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_fr2wv_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
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
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_name'] = 'test_data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'wcnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_test'
            input_data['nn_wf_node_name'] = 'pre_feed_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2wcnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_train'
            input_data['nn_wf_node_name'] = 'pre_feed_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_fr2wcnn'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0

            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
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
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_iob'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_name'] = 'test_data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_iob'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'bilstmcrf'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_test'
            input_data['nn_wf_node_name'] = 'pre_feed_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_iob2bilstmcrf'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_train'
            input_data['nn_wf_node_name'] = 'pre_feed_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_iob2bilstmcrf'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
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
            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_name'] = 'data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.train_data
            self.__put_nn_wf_node_info(input_data)

            # data node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_name'] = 'test_data_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.eval_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'fasttext'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_test'
            input_data['nn_wf_node_name'] = 'pre_feed_test'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_iob2bilstmcrf'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_eval_data
            self.__put_nn_wf_node_info(input_data)

            # feed node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_pre_feed_train'
            input_data['nn_wf_node_name'] = 'pre_feed_train'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'pre_feed_text2fasttext'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            input_data['nn_wf_node_desc'] = self.feed_train_data
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_extra'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_train'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_train'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_test_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_pre_feed_test'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_pre_feed_test'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_eval_node'
            self.__put_nn_wf_node_relation(input_data)
        except Exception as e:
            raise Exception(e)
        finally:
            return True