from cluster.service.service_predict_seq2seq import PredictNetSeq2Seq
from chatbot.common.chat_share_data import ShareData

class IntendAnalyzer(ShareData):

    """
    parse raw text to tageed, entity filterd sentence
    ※ Example
    input : I bought a car yesterday
    output : I bought a car [time]
    """

    def __init__(self, nn_id):
        """
        init global variables
        """
        self.nn_id = ""
        self.seq2seq_model = PredictNetSeq2Seq()

    def parse(self, share_data):
        """
        run intent analyzer
        :param context:
        :return:
        """

        return share_data

