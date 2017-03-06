from django.core.cache import cache

class ClusterServerConf :
    """
    1. desc : CRUD function for server table
    2. table : CONF_SERV_CLUSTER_INFO
    """

    def server_start_up(self):
        self.mount_cache()

    def mount_cache(self):
        """

        :return:
        """
        # cache.set("key", "value", "time")

    def get_all_list(self):
        """
        retun all data as model object form
        :return:model objects
        """
        # obj = models.JobManagement.objects
        return None

    def insert_server_info(self, server_obj):
        """
        insert server info
        :return:
        """
        return None

    def update_server_info(self, server_obj):
        """
        update server info
        :return:
        """
        return None

    def delete_server_info(self, server_name):
        """
        delete serer info
        :return:
        """
        return None

    def update_server_status(self, server_name, status):
        """
        excepted to called from data connection manger, if connection works set true, else set false
        :return:
        """
        return None