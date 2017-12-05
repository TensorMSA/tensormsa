from cluster.service.service_predict import PredictNet
from third_party.ngram.ngram_compare_mro import ThirdPartyNgram

class PredictNetNgram(PredictNet):
    def run(self, nn_id, parm):
        """
        run predict service
        1. get node id
        2. check json conf format
        3. run predict & return
        :param parm:
        :return:
        """
        if(self._valid_check(parm)) :
            if (nn_id == 'mro_compare'):
                return ThirdPartyNgram().predict(nn_id, parm)
            else:
                None

    def _valid_check(self, parm):
        return True