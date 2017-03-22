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
        error_msg = ""
        if ('type' not in parm):
            error_msg = ''.join([error_msg, 'type (vector, sim, train) not defined'])
        if ('val_1' not in parm):
            error_msg = ''.join([error_msg, 'val_1 not defined'])
        if ('val_2' not in parm):
            error_msg = ''.join([error_msg, 'val_2 not defined'])
        if(error_msg == "") :
            return True
        else :
            raise Exception(error_msg)

