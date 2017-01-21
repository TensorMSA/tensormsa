
class WorkFlowDataImage :
    """
    1. Definition
    handle preview and settings for image data
    2. Tables
    NN_WF_NODE_INFO (NODE_CONFIG_DATA : Json Field) 
    """

    def get_lable_list(self):
        """

        :return:
        """
        return []

    def get_preview_urls(self):
        """

        :return:
        """
        return []

    def save_all(self, obj):
        """

        :param obj:
        :return:
        """
        self._insert_preview_images()
        self._set_preivew_paths()
        self._set_lable_list()
        self._set_preprocess_info()
        self._set_target_store_info()
        return None

    def _insert_preview_images(self):
        """

        :return:
        """
        return None

    def _set_preivew_paths(self, preview_path_list):
        """

        :param preview_path_list:
        :return:
        """
        return None

    def _set_lable_list(self, lable_list):
        """

        :param lable_list:
        :return:
        """
        return None

    def _set_preprocess_info(self, preprocess_info):
        """

        :param preprocess_info:
        :return:
        """
        return None

    def _set_target_store_info(self, store_info):
        """

        :param store_info:
        :return:
        """
        return None