from django.core.cache import cache
from django.conf import settings
import os

class MasterServerConf() :
    """
    1. desc : CRUD function for server table
    2. table : CONF_SERV_DATA_INFO
    """

    def server_start_up(self):
        self.mount_cache()


    def get_nas_conf(self):
        """

        :return:
        """
        return None

    def get_rdb_conf(self):
        """

        :return:
        """
        return None

    def get_data_mart_conf(self):
        """

        :return:
        """
        return None

    def update_nas_conf(self):
        """

        :return:
        """
        return None

    def update_rdb_conf(self):
        """

        :return:
        """
        return None

    def update_data_mart_conf(self):
        """

        :return:
        """
        return None

    def insert_nas_conf(self):
        """

        :return:
        """
        return None

    def insert_rdb_conf(self):
        """

        :return:
        """
        return None

    def insert_data_mart_conf(self):
        """

        :return:
        """
        return None

    def delete_nas_conf(self):
        """

        :return:
        """
        return None

    def delete_rdb_conf(self):
        """

        :return:
        """
        return None

    def delete_data_mart_conf(self):
        """

        :return:
        """
        return None

    def mount_cache(self):
        """

        :return:
        """
        if(os.path.exists("/hoya_src_root") == False) :
            os.mkdir("/hoya_src_root")
        if(os.path.exists("/hoya_str_root") == False) :
            os.mkdir("/hoya_str_root")
        if (os.path.exists("/hoya_model_root") == False):
            os.mkdir("/hoya_model_root")

        cache.set("source_root", "/hoya_src_root")
        cache.set("store_root", "/hoya_str_root")
        cache.set("model_root", "/hoya_model_root")