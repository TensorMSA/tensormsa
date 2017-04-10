from master.workflow.common.workflow_common import WorkFlowCommon

class WorkFlowData(WorkFlowCommon) :
    """

    """

    def get_node_status(self):
        """
        return node status info (nn_id, nn_ver, node_type, node_prg, etc)
        :return:
        """
        return None

    def get_preview_data(self):
        """
        extract data from target server
        1. connect datastore (use common data manager)
        2. return limited number of data from source
        :return:
        """
        pass

    def set_preview_data(self):
        """
        extract data from target server
        1. connect datastore (use common data manager)
        2. return limited number of data from source
        :return:
        """
        pass

    def get_step_source(self):
        """
        getter for source step
        :return:obj(json) to make view
        """
        pass

    def put_step_source(self, obj):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """
        pass

    def check_step_source(self, obj):
        """
        check step_source process fit to requirement
        :param obj: config data from view
        :return:boolean
        """
        pass

    def get_step_preprocess(self):
        """
        getter for preprocess
        :return:obj(json) to make view
        """
        pass

    def check_step_preprocess(self, obj):
        """
        check step_source process fit to requirement
        :param obj: config data from view
        :return:boolean
        """
        pass

    def put_step_preprocess(self, obj):
        """
        putter for preprocess
        :param obj: config data from view
        :return:boolean
        """
        pass

    def get_step_store(self):
        """
        getter for store
        :return:obj(json) to make view
        """
        pass

    def check_step_store(self, obj):
        """
        check step_source process fit to requirement
        :param obj: config data from view
        :return:boolean
        """
        pass

    def put_step_store(self, obj):
        """
        putter for store
        :param obj: config data from view
        :return:boolean
        """
        pass