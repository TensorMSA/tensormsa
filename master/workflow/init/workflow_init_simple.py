from django.core import serializers as serial
from master import models
from master import serializers
from django.db import connection
from common.utils import dictfetchall
import json

class WorkFlowSimpleManager :
    """

    """
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
        elif(type == 'renet'):
            self._create_predefined_nodes_renet(state_id)
        elif(type == 'word2vec'):
            self._create_predefined_nodes_word2vec(state_id)
        elif(type == 'doc2vec'):
            self._create_predefined_nodes_doc2vec(state_id)
        elif (type == 'frame'):
            self._create_predefined_nodes_frame(state_id)
        elif (type == 'seq2seq'):
            self._create_predefined_nodes_seq2seq(state_id)
        else :
            raise Exception ("Error : Not defined type ")

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
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_name'] = 'datasrc'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'data_image'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'nf_cnn'
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
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
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

    def _create_predefined_nodes_renet(self, wf_state_id):
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
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_netconf_node'
            input_data['nn_wf_node_name'] = 'netconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'nf_renet'
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
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_datasrc'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
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

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
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
            input_data['wf_task_submenu_id'] = 'data_text'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
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

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
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
            self.__put_nn_wf_node_info(input_data)

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_dataconf_node'
            input_data['nn_wf_node_name'] = 'dataconf_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'df_frame'
            input_data['wf_node_status'] = 0
            input_data['node_config_data'] = {}
            input_data['node_draw_x'] = 0
            input_data['node_draw_y'] = 0
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
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_data_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_dataconf_node'
            self.__put_nn_wf_node_relation(input_data)

            input_data = {}
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['nn_wf_node_id_1'] = str(wf_state_id) + '_dataconf_node'
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
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

            # net conf node
            input_data = {}
            input_data['nn_wf_node_id'] = str(wf_state_id) + '_eval_node'
            input_data['nn_wf_node_name'] = 'eval_node'
            input_data['wf_state_id'] = str(wf_state_id)
            input_data['wf_task_submenu_id'] = 'eval_ran'
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
            input_data['nn_wf_node_id_2'] = str(wf_state_id) + '_netconf_node'
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
