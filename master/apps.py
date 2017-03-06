from django.apps import AppConfig
from master.server.master_server_conf import MasterServerConf
from master.server.cluster_server_conf import ClusterServerConf
from master.server.data_server_conf import DataServerConf

class MasterConfig(AppConfig):
    name = 'master'

    def ready(self):
        """
        set cache on server start up
        :return:
        """
        MasterServerConf().server_start_up()
        ClusterServerConf().server_start_up()
        DataServerConf().server_start_up()