from cluster.service.service_predict import PredictNet
from cluster.neuralnet.neuralnet_node_residual import NeuralNetNodeReNet

class PredictNetRenet(PredictNet):
    def run(self, nn_id, ver, parm):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        if(self._valid_check(parm)) :
            return NeuralNetNodeReNet().predict(self._find_netconf_node_id(nn_id), parm)

    def _valid_check(self, parm):
        return True