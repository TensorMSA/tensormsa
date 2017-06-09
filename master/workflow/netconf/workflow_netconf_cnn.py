from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from common.utils import *
from master import models
from django.core import serializers as serial
import json

class WorkFlowNetConfCNN(WorkFlowNetConf):
    """

    """
    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms([])
        self._set_prhb_parms([])

    def set_num_classes_predcnt(self, nn_id, wfver, node, node_id, netconf):
        try:
            labels = netconf["labels"]
            num_classes = netconf["config"]["num_classes"]
            pred_cnt = netconf["param"]["predictcnt"]

            if len(labels) > num_classes:
                num_classes = len(labels)
            if pred_cnt > len(labels):
                pred_cnt = len(labels)

            netconf["config"]["num_classes"]=num_classes
            netconf["param"]["predictcnt"]=pred_cnt
        except:
            None

        netconf["modelpath"] = get_model_path(nn_id, wfver, node)
        netconf["modelname"] = nn_id + "_" + wfver

        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)

        setattr(obj, "node_config_data", netconf)
        obj.save()
        return netconf

    def set_view_obj_path(self, nn_id, wfver, node, node_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        self.validation_check(input_data)
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        try:
            old_config_data = getattr(obj, 'node_config_data')
            if len(input_data["labels"]) == 0:
                input_data["labels"] = old_config_data["labels"]
        except:
            None

        setattr(obj, "node_config_data", input_data)
        obj.save()
        return input_data