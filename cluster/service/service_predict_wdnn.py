from cluster.service.service_predict import PredictNet

class PredictNetWdnn(PredictNet):
    """

    """

    def run(self, nn_id, parm={}):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        if(self._valid_check(parm)) :
            return None

    def _valid_check(self, parm):
        return True

