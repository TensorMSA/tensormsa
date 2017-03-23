from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedFr2Wdnn(WorkFlowPre):
    """

    """

    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        self.key = key

    def validation_check(self, json_data):
        error_msg = ""

        if(error_msg == "") :
            return True
        else :
            raise Exception (error_msg)
