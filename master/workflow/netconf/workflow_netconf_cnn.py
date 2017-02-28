from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from common.utils import *
from master import models
from django.core import serializers as serial
import json

class WorkFlowNetConfCNN(WorkFlowNetConf):
    """

    """
    def get_view_obj(self, input_data):
        """
        get view data for net config
        :return:
        """
        nn_id = input_data["key"]["nn_id"]
        wf_ver_id = input_data["key"]["wf_ver_id"]
        node_id = input_data["key"]["node_id"]
        state_id = nn_id + "_" + wf_ver_id

        println("WorkFlowNetConfCNN get_view_obj nn_id="+nn_id+" wf_ver_id="+wf_ver_id+" node_id="+node_id+" state_id="+state_id)

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(wf_state_id_id=state_id, nn_wf_node_id=node_id)
            data_set = getattr(obj, "node_config_data")
            return data_set
        except Exception as e:
            raise Exception(e)
        return None

    def set_view_obj(self, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        nn_id = input_data["key"]["nn_id"]
        wf_ver_id = input_data["key"]["wf_ver_id"]
        node_id = input_data["key"]["node_id"]
        state_id = nn_id+"_"+wf_ver_id

        println("WorkFlowNetConfCNN set_view_obj nn_id="+nn_id+" wf_ver_id="+wf_ver_id+" node_id="+node_id+" state_id="+state_id)

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(wf_state_id_id=state_id, nn_wf_node_id=node_id)
            setattr(obj, "node_config_data", input_data)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)
        return None

