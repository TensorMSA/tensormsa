from master.workflow.data.workflow_data import WorkFlowData

class WorkFlowDataText(WorkFlowData) :
    """
    1. Definition
    Reuse already saved as HDF5 format
    2. Tables
    NN_WF_NODE_INFO (NODE_CONFIG_DATA : Json Field)
    """


    def load_data(self, type, conn):
        """

        :param type:
        :param conn:
        :return:
        """
        return None


    def get_step_source(self):
        """
        getter for source step
        :return:obj(json) to make view
        """
        return None


    def put_step_source(self, obj):
        """
        putter for source step
        :param obj: config data from view
        :return:boolean
        """
        return None


    def get_step_preprocess(self):
        """
        getter for preprocess
        :return:obj(json) to make view
        """
        return None


    def put_step_preprocess(self, obj):
        """
        putter for preprocess
        :param obj: config data from view
        :return:boolean
        """
        return None


    def get_step_store(self):
        """
        getter for store
        :return:obj(json) to make view
        """
        return None


    def put_step_store(self, obj):
        """
        putter for store
        :param obj: config data from view
        :return:boolean
        """
        return None