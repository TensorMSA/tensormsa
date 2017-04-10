from common.utils import *
from master import models
from master.workflow.common.workflow_common import WorkFlowCommon

class WorkFlowPre(WorkFlowCommon) :

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms([])
        self._set_prhb_parms([])