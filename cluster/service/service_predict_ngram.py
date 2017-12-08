from cluster.service.service_predict import PredictNet
from third_party.ngram.ngram_compare_mro import ThirdPartyNgram

class PredictNetNgram(PredictNet):
    def run(self, type, nn_id, ver, parm):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        if(self._valid_check(parm)) :
            return ThirdPartyNgram().predict(type, nn_id, ver, parm)

    def _valid_check(self, parm):
        return True