from cluster.neuralnet.neuralnet_node_cnn import NeuralNetNodeCnn
from cluster.service.service_predict import PredictNet
from common.utils import *
from master import models
import logging

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
        logging.info("2. PredictNetCnn Start : {0}".format(parm))
        return NeuralNetNodeCnn().predict(self._find_netconf_node_id(nn_id, ver), parm)

    def _valid_check(self, parm):
        return True

