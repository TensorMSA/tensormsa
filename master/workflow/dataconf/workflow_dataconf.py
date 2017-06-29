from master import models
from common import utils
from master.workflow.common.workflow_common import WorkFlowCommon

class WorkFlowDataConf(WorkFlowCommon) :

    # def __init__(self, key = None):
    #     """
    #     init key variable
    #     :param key:
    #     :return:
    #     """
    #     self.key = key
    #     self.conf = self.get_step_source(key)

    # @property
    # def data_conf(self):
    #     """
    #     getter for preprocess
    #     """
    #     return self.conf['data_conf']

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


