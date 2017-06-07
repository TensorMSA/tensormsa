from cluster.neuralnet.neuralnet_node_wdnn import NeuralNetNodeWdnn
from cluster.service.service_predict import PredictNet
from master import models

class PredictNetWdnn(PredictNet):
    """

    """

    def run(self, nn_id, ver, parm={}):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """

        # if(self._valid_check(parm)) :
        netconf_arr =[]
        dataconf_arr = []

        # query_set = models.NN_WF_NODE_INFO.objects.filter(wf_state_id=nn_id + "_" + ver)
        net_conf = models.NN_WF_NODE_INFO.objects.filter(nn_wf_node_id = nn_id + "_" + ver + "_netconf_node")
        for data in net_conf:
            netconf_arr = data.node_config_data

        data_conf = models.NN_WF_NODE_INFO.objects.filter(nn_wf_node_id = nn_id + "_" + ver + "_dataconf_node")
        for data in data_conf:
            dataconf_arr = data.node_config_data

        conf_data = {}
        conf_data['node_id'] = nn_id
        conf_data['net_conf'] = netconf_arr
        conf_data['data_conf'] = dataconf_arr


        if(self._valid_check(parm)) :
            return NeuralNetNodeWdnn().predict(nn_id, ver, parm)

    def _valid_check(self, parm):
        return True

