
class WorkFlowEasyRuleManager :
    """
    2. Related Tables : NN_WF_EASYMODE_RULE

    """

    def _get_purp_list(self):
        """
        get distinct list of purpose
        :return:list
        """

        return []

    def _get_datatype_list(self):
        """
        get distinct data type list
        :return: list
        """
        return []

    def _get_storetype_list(self):
        """
        get distinct store type list
        :return: list
        """
        return []

    def _get_data_size_list(self):
        """
        get distinct data size list
        :return: list
        """
        return []

    def get_easy_wf_menu(self):
        """
        return composed data set of menu info
        :return: json
        """
        self._get_data_size_list()
        self._get_datatype_list()
        self._get_purp_list()
        self._get_storetype_list()

        return None

    def get_wf_code_with_option(self, option):
        """
        recommned wf code (predefined) based on user selection
        :param option: object
        :return: str
        """

        return None

