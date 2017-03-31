from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from common.utils import *
from master import models
from django.core import serializers as serial
import json

class WorkFlowNetConfCNN(WorkFlowNetConf):
    """

    """
    def set_num_classes_predcnt(self, netconf, dataconf):
        self.validation_check(netconf)
        labels = dataconf["labels"]
        num_classes = netconf["config"]["num_classes"]
        pred_cnt = netconf["config"]["predictcnt"]

        if len(labels) > num_classes:
            num_classes = len(labels)
        if pred_cnt > len(labels):
            pred_cnt = len(labels)

        netconf["config"]["num_classes"] = num_classes
        netconf["config"]["predictcnt"] = pred_cnt

        nn_id = netconf["key"]["nn_id"]
        wfver = netconf["key"]["wf_ver_id"]
        node = netconf["key"]["node"]
        node_id = nn_id+'_'+wfver+'_'+node
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)

        setattr(obj, "node_config_data", netconf)
        obj.save()
        return netconf

    def set_view_obj(self, node_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        try:
            self.validation_check(input_data)
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
            nn_id = input_data["key"]["nn_id"]
            wfver = input_data["key"]["wf_ver_id"]
            node = input_data["key"]["node"]
            input_data["modelpath"] = get_model_path(nn_id, wfver, node)
            input_data["modelname"] = "model_"+nn_id+"_"+wfver
            setattr(obj, "node_config_data", input_data)
            obj.save()
            return input_data
        except Exception as e:
            raise Exception(e)
        return None


    def validation_check(self, json_data):
        return True