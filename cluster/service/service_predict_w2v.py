from cluster.neuralnet.neuralnet_node_w2v import NeuralNetNodeWord2Vec
from cluster.service.service_predict import PredictNet


class PredictNetW2V(PredictNet):
    """

    """

    def run(self, nn_id, parm = {}):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        if(self._valid_check(parm)) :
            return NeuralNetNodeWord2Vec().predict(self._find_netconf_node_id(nn_id), parm)

    def _valid_check(self, parm):
        return True

