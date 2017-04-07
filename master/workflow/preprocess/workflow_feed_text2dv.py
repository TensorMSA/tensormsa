from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedText2Dv(WorkFlowPre):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key
        self._set_essence_parms([])
        self._set_update_prohibited_ids([])