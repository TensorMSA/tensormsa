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
        self._set_essence_parms([])
        self._set_update_prohibited_ids([])