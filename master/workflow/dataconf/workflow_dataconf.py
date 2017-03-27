from master import models
from common import utils


class WorkFlowDataConf :

    # def __init__(self, key = None):
    #     """
    #     init key variable
    #     :param key:
    #     :return:
    #     """
    #     self.key = key
    #     self.conf = self.get_step_source(key)

    def get_step_source(self, nnid):
        """
        getter for source step
        :return:obj(json) to make view
        """
        #TODO : NNID는 안씀
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
            config_data = getattr(obj, 'node_config_data')
            return config_data
        except Exception as e:
            raise Exception(e)

    @property
    def data_conf(self):
        """
        getter for preprocess
        """
        return self.conf['data_conf']


    def get_node_status(self):
        """
        return node status info (nn_id, nn_ver, node_type, node_prg, etc)
        :return:
        """
        return None

    def get_related_node_status(self):
        """
        get related node info (especially data node)
        :return:object (related node's data info)
        """
        return None


    def get_view_obj(self):
        """
        get column type info for view
        :return:
        """
        pass



    def set_view_obj(self, obj):
        """
        set column type info on db json filed
        :param obj:
        :return:
        """
        pass

    def validation_check(self, json_data):
        pass