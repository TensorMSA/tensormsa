from cluster.neuralnet.neuralnet_node_autoencoder import NeuralNetNodeAutoEncoder as AutoEncoder
from cluster.service.service_predict import PredictNet

class PredictNetAutoEncoder(PredictNet):
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
            return AutoEncoder().predict(self._find_netconf_node_id(nn_id), parm)

    def _valid_check(self, parm):
        error_msg = ""
        if ('input_data' not in parm):
            error_msg = ''.join([error_msg, 'input_data (str) not defined'])

        if(error_msg == "") :
            return True
        else :
            raise Exception(error_msg)
