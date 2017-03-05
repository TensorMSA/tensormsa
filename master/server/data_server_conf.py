

class DataServerConf :
    """
    1. desc : CRUD function for server table
    2. table : CONF_SERV_DATA_INFO
    """

    def server_start_up(self):
        self.mount_cache()

    def get_selected_object(self):
        """

        :return:
        """
        return None

    def get_all_list(self):
        """
        retun all data as model object form
        :return:model objects
        """
        # obj = models.JobManagement.objects
        return None

    def get_selected_list(self, type):
        """
        return selected type of server info
        :return:model objects
        """
        # obj = models.JobManagement.objects.get(nn_id=str(nn_id))
        return None

    def get_hbase_server_list(self):
        """
        return objects filterd with type (use master.util.CodeRuleManager to get code id of 'hbase')
        :return: objects
        """
        return None

    def get_s3_server_list(self):
        """
        return objects filterd with type (use master.util.CodeRuleManager to get code id of 'S3')
        :return:
        """
        return None

    def get_redis_server_list(self):
        """
        return objects filterd with type (use master.util.CodeRuleManager to get code id of 'redis')
        :return:
        """
        return None


    def get_oracle_rdb_list(self):
        """
        return objects filterd with type (use master.util.CodeRuleManager to get code id of 'rdb')
        :return:
        """
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

    def mount_cache(self):
        """

        :return:
        """

        # cache.set("key", "value", "time")