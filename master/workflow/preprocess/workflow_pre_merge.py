from master.workflow.preprocess.workflow_pre import WorkFlowPre

class WorkFlowPreMerge(WorkFlowPre):
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
        if('batchsize' not in json_data) :
            error_msg = ''.join([error_msg, 'batchsize (int) not defined'])
        if('merge_rule' not in json_data) :
            error_msg = ''.join([error_msg, 'merge_rule (dict) not defined'])
        if('type' not in json_data) :
            error_msg = ''.join([error_msg, 'type (str) not defined'])

        if(error_msg == "") :
            return True
        else :
            return error_msg

    def get_batchsize(self):
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['batchsize']

    def get_merge_rule(self):
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['merge_rule']

    def get_type(self):
        if('conf' not in self.__dict__) :
            self.conf = self.get_view_obj(self.key)
        return self.conf['type']

    def get_state_code(self):
        if('state_id' not in self.__dict__) :
            self.state_id = self.get_state_id(self.key)
        return self.state_id

