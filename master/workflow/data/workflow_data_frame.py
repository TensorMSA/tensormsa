from master.workflow.data.workflow_data import WorkFlowData


class WorkFlowDataFrame(WorkFlowData) :
    """
    1. Definition
    handle preview and settings for frame data
    2. Tables
    NN_WF_NODE_INFO (NODE_CONFIG_DATA : Json Field)
    """


    def get_preview_data(self):
        """

        :param type:
        :param conn:
        :return:
        """
        return None


    def set_preview_data(self):
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

    def _load_local_frame(self, conn):

        return None

    def _load_s3_frame(self, conn):

        return None

    def _load_rdb_frame(self, conn):

        return None

    def _load_hbase_frame(self, conn):

        return None

    def _set_default_column_type(self):

        return None