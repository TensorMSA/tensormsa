from master.workflow.dataconf.workflow_dataconf import WorkFlowDataConf

class WorkflowDataConfFrame(WorkFlowDataConf):
    """

    """
    def get_view_obj(self):
        """
        get column type info for view
        :return:
        """
        self._get_default_type()
        self._get_modified_type()

        return None

    def set_view_obj(self, obj):
        """
        set column type info on db json filed
        :param obj:
        :return:
        """
        return None

    def _get_lable_list(self):
        """

        :return:
        """
        return None

    def _get_unlable_list(self):
        """

        :return:
        """
        return None


    def _get_semi_rule(self):
        """

        :return:
        """
        return None

    def _set_lable_list(self):
        """

        :return:
        """
        return None

    def _set_unlable_list(self):
        """

        :return:
        """
        return None

    def _set_semi_rule(self):
        """

        :return:
        """
        return None