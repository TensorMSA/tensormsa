from master.workflow.netconf.workflow_netconf import WorkFlowNetConf
from master import models
from common.utils import *


class WorkFlowNetConfXgboost(WorkFlowNetConf):
    """

    """
    @property
    def node_config_data(self):
        """
        getter for learning_rate
        """
        return self.conf


    def __init__(self, key = None):
        """
        init key variable
        :param key:
        :return:
        """
        if key is not None :
            self.key = key
            self.conf = self.get_step_source(key)

        self._set_prhb_parms(['model_path', 'encoder_len', 'decoder_len','encoder_depth', 'cell_type'])



    def get_step_source(self, nnid):
        """
        getter for source step
        :return:obj(json) to make view
        """
        try:
            obj = models.NN_WF_NODE_INFO.objects.get(nn_wf_node_id=self.key)
            config_data = getattr(obj, 'node_config_data')
            return config_data
        except Exception as e:
            raise Exception(e)



