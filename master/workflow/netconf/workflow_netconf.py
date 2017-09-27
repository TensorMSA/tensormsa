from common.utils import *
from master import models
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