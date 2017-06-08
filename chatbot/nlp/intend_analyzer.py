from cluster.service.service_predict_seq2seq import PredictNetSeq2Seq
from cluster.service.service_predict_wcnn import PredictNetWcnn
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
        self.wcnn_model = PredictNetWcnn()

    def parse(self, share_data):
        """
        run intent analyzer
        :param context:
        :return:
        """
        if (share_data.get_story_id() != ""):
            print("■■■■■■■■■■ 의도 존재  : " + share_data.get_story_id())
        else :
            convert_data =  share_data.get_convert_data()
            # TODO : get data from db
            #result = self.seq2seq_model.run(self.nn_id , {"input_data": convert_data, "num": 0, "clean_ans": False})[0][1][0]
            result = str(self.wcnn_model.run(self.nn_id , {"input_data": convert_data, "num": 0, "clean_ans": False}))
            print ("■■■■■■■■■■ 의도 분석 결과 : " + result)
            share_data.set_intent_id(result)
            share_data.set_intent_history(result)
        return share_data

