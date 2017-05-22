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
        self.nn_id = nn_id
        self.seq2seq_model = PredictNetSeq2Seq()

    def parse(self, share_data):
        """
        run intent analyzer
        :param context:
        :return:
        """
        if (share_data.get_story_id() != "") :
            print("■■■■■■■■■■ 의도 존재 : " + share_data.get_story_id())
        else :
            convert_data =  share_data.get_convert_data()
            result = self.seq2seq_model.run(self.nn_id , {"input_data": convert_data, "num": 0, "clean_ans": False})
            print ("■■■■■■■■■■ 의도 분석 결과 : " + result[0][1][0])
            share_data.set_intent_id(result[0][1][0])
            share_data.set_intent_history(result[0][1][0])
        return share_data

