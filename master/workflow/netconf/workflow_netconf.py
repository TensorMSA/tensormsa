from common.utils import *
from master import models
import json
from django.core import serializers as serial
from master.workflow.common.workflow_common import WorkFlowCommon

class WorkFlowNetConf(WorkFlowCommon) :

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms([])
        self._set_prhb_parms([])

    def set_view_obj_node(self, node_id, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        # self.validation_check(input_data)
        obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=node_id)
        setattr(obj, "node_config_data", input_data)
        obj.save()
        return input_data

    def set_node_config_single(self, nnid, ver, input_data):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        query_set = models.AUTO_ML_RULE.objects.filter(graph_flow_id=input_data["type"])
        query_set = serial.serialize("json", query_set)
        query_set = json.loads(query_set)
        ids = []
        for row in query_set:
            single = row['fields']['graph_flow_data_single']
            for col in single:
                node_id = nnid + '_' + ver + '_' + col
                self.set_view_obj_node(node_id, single[col])
                print(col)


        return input_data