from master.workflow.data.workflow_data import WorkFlowData

class WorkFlowDataReuse(WorkFlowData) :
    """
    1. Definition
    Reuse already saved as HDF5 format
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

    def _set_reuse_data_conf(self, nn_id, nn_ver, cate, subcate, table):
        """
        copy data conf from selected data(preprocessed HDF5) to
        own network related data field
        :param nn_id: own nn_id
        :param nn_ver: own nn_version
        :param cate: copy target category
        :param subcate: copy target subcategory
        :param table: copy target table
        :return:
        """
        return None

    def _get_reuse_data_conf(self):
        """
        get selected networks data info
        (conf info : conn, path, etc.. )
        :return:
        """
        return None

