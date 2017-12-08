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
        if(self._valid_check(parm)) :
            if ver == 'active':
                condition = {'nn_id': nn_id}
                ver = NNCommonManager().get_nn_info(condition)[0]['nn_wf_ver_id']

            return NeuralNetNodeImage().predict(nn_id, ver, parm)

    def _valid_check(self, parm):
        return True