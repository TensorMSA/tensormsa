from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedIob2BiLstmCrf(WorkFlowPre):
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