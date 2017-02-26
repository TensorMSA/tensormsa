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
        if(type == 'image'):
            self._create_predefined_nodes_image(state_id)

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

    def _create_predefined_nodes_nlp(self, wf_state_id):
        """

        :return:
        """
        pass

    def _create_predefined_nodes_frame(self, wf_state_id):
        """

        :return:
        """
        pass


    def _create_predefined_nodes_image(self, wf_state_id):
        """

        :return:
        """
        try:
            # data node
            self.__create_node_data_img(wf_state_id)
            # net conf node
            self.__create_node_nn_cnn(wf_state_id)
        except Exception as e:
            raise Exception(e)
        finally:
            return True


    def __put_NN_WF_NODE_INFO(self, input_data):
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

    def __create_node_data_img(self, wf_state_id):
        """

        :return:
        """
        input_data = {}
        input_data['nn_wf_node_name'] = 'data_node'
        input_data['wf_state_id'] = str(wf_state_id)
        input_data['wf_task_submenu_id'] = 'data_image'
        input_data['wf_node_status'] = 0
        input_data['node_config_data'] = {}
        input_data['node_draw_x'] = 0
        input_data['node_draw_y'] = 0
        self.__put_NN_WF_NODE_INFO(input_data)


    def __create_node_nn_cnn(self, wf_state_id):
        """

        :return:
        """
        input_data = {}
        input_data['nn_wf_node_name'] = 'netconf_node'
        input_data['wf_state_id'] = str(wf_state_id)
        input_data['wf_task_submenu_id'] = 'nf_cnn'
        input_data['wf_node_status'] = 0
        input_data['node_config_data'] = {}
        input_data['node_draw_x'] = 0
        input_data['node_draw_y'] = 0
        self.__put_NN_WF_NODE_INFO(input_data)