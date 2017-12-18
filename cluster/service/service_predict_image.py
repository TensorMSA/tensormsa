from cluster.service.service_predict import PredictNet
from cluster.neuralnet.neuralnet_node_image import NeuralNetNodeImage
from master.network.nn_common_manager import NNCommonManager

class PredictNetImage(PredictNet):
    def run(self, nn_id, ver, parm):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        if(self._valid_check(parm.FILES)) :
            return NeuralNetNodeImage().predict(nn_id, ver, parm.FILES)

    def _valid_check(self, parm):
        return True