from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkflowFeedFr2Seq(WorkFlowPre):
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
        if('encode_column' not in json_data) :
            error_msg = ''.join([error_msg, 'encode_column not defined'])
        if('decode_column' not in json_data) :
            error_msg = ''.join([error_msg, 'decode_column not defined'])

        if(error_msg == "") :
            return True
        else :
            raise Exception(error_msg)
