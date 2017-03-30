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

    def validation_check(self, json_data):
        return True