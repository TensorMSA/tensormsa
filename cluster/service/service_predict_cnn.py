from cluster.neuralnet.neuralnet_node_cnn import NeuralNetNodeCnn
from cluster.service.service_predict import PredictNet
from common.utils import *
from master import models

class PredictNetCnn(PredictNet):
    """

    """

    def run(self, nn_id, ver, parm):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        # if(self._valid_check(parm)) :
        return_arr = []
        query_set = models.NN_WF_NODE_RELATION.objects.filter(wf_state_id=nn_id + "_" + ver)
        for data in query_set:
            if (len(return_arr) == 0):
                return_arr.append(data.nn_wf_node_id_1)
                return_arr.append(data.nn_wf_node_id_2)
            else:
                if ((data.nn_wf_node_id_1 in return_arr) and return_arr.index(data.nn_wf_node_id_1) >= 0):
                    idx = return_arr.index(data.nn_wf_node_id_1)
                    return_arr.insert(idx + 1, data.nn_wf_node_id_2)
                elif ((data.nn_wf_node_id_2 in return_arr) and return_arr.index(data.nn_wf_node_id_2) >= 0):
                    idx = return_arr.index(data.nn_wf_node_id_2)
                    return_arr.insert(idx, data.nn_wf_node_id_1)

        conf_data = {}
        conf_data['node_id'] = nn_id
        conf_data['node_list'] = return_arr

        return NeuralNetNodeCnn().predict(conf_data, ver, parm)

    def _valid_check(self, parm):
        return True

