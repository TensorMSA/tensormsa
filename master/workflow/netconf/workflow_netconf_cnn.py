from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from common.utils import *
from master import models
from django.core import serializers as serial
import json

class WorkFlowNetConfCNN(WorkFlowNetConf):
    """

    """
    def get_view_obj(self, node_id):
        """
        get view data for net config
        :return:
        """
        # node_id = input_data["key"]["node_id"]

        println("WorkFlowNetConfCNN get_view_obj node_id="+node_id)

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
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
        node_id = input_data["key"]["node_id"]

        println("WorkFlowNetConfCNN set_view_obj node_id="+node_id)

        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            setattr(obj, "node_config_data", input_data)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)
        return None

