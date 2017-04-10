from master import models
from master.workflow.common.workflow_common import WorkFlowCommon

class WorkFlowEvalConfig(WorkFlowCommon):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_key_parms(['type'])
        self._set_prhb_parms(['type'])

    def get_eval_type(self):
        """
        get eval type ( regression, classification.. )
        :return:
        """
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf.get('type')